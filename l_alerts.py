import smtplib
import ssl

import l_baselinker
import datetime

from jinja2 import Environment, FileSystemLoader

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class BaselinkerAlert:


    def __init__(self, statuses, time_to_search) -> None:
        self.statuses = statuses
        self.sender = "ALERTER"
        self.subject = "ALERT"
        self.recepients = [
            'johndoe@gmail.com',
        ]
        self.get_invoice = False
        self.get_status_name = False


        self.template_root_path = "/home/user1/Desktop/refac/baselinker_alerty/templates"
        self.text_template_path = None
        self.html_template_path = None

        self.text_preprocessor = None
        self.html_preprocessor = None

        self.smtp_login = "johndoe@gmail.com"
        self.smtp_password = ""

        self.time_to_search = time_to_search

        self.dev_limit = None

    
    def _get_baselinker_orders_for_status(self, status_id):
        orders = l_baselinker.baselinker_request("getOrders", {
            "status_id": status_id,
            "get_unconfirmed_orders": True
        }).json()['orders']
        orders_ids = [x['order_id'] for x in orders]
        conn = len(orders) == 100
        while conn:
            orders_temp_raw = l_baselinker.baselinker_request("getOrders", {
                "status_id": status_id,
                "get_unconfirmed_orders": True,
                "id_from": orders_ids[-1]
            }).json()['orders']
            for x in orders_temp_raw:
                order_id = x['order_id']
                if order_id in orders_ids:
                    continue
                orders.append(x)
                orders_ids.append(order_id)
            conn = len(orders_temp_raw) == 100
        return orders
    
    def _get_baselinker_status_name(self, status_id):
        baselinker_status_request = l_baselinker.baselinker_request("getOrderStatusList").json()['statuses']
        baselinker_status_request = [x['name'] for x in baselinker_status_request if x['id'] == int(status_id)]
        try:
            return baselinker_status_request[0]
        except:
            return None

    def _get_baselinker_invoice_for_order_id(self, order_id):
        invoices = l_baselinker.baselinker_request("getInvoices", {
        "order_id": order_id
        }).json()['invoices']
        try:
            return invoices[0]['number']
        except:
            return None


    def _send_alert(self, msg):
        sslContext = ssl.create_default_context()
        connection = smtplib.SMTP("smtp.dpoczta.pl", "587")
        connection.starttls(context=sslContext)
        connection.login(self.smtp_login, self.smtp_password)

        email_sender = "{} <{}>".format(self.sender, self.smtp_login)

        msg['Subject'] = self.subject
        msg['From'] = email_sender



        connection.sendmail(email_sender, self.recepients, msg.as_string())
        connection.close()


    def _create_internal_order(self, order, fv, status_name):
        order_id = order['order_id']
        order_add_date = datetime.datetime.fromtimestamp(order['date_add'])
        order_status_date = datetime.datetime.fromtimestamp(order['date_in_status'])
        return {
            "id": order_id,
            "add_date": order_add_date,
            "status_date": order_status_date,
            "status_name": status_name,
            "fv": fv
        }
        # return (order_id, order_add_date, order_status_date, status_name, fv)



    def _check_if_order_meets_requirements(self, order):
        order_status_date = datetime.datetime.fromtimestamp(order['date_in_status'])
        return order_status_date < self.time_to_search

    def _load_template(self, template_path):
        env = Environment(
            loader=FileSystemLoader(self.template_root_path)
        )
        return env.get_template(template_path)
    

    def _create_text_message(self, alerts, is_dict_type):
        temp = self._load_template(self.text_template_path)
        ARGS_TO_RENDER = self.text_preprocessor(alerts, is_dict_type)
        rendered_content = temp.render(**ARGS_TO_RENDER)
        return MIMEText(rendered_content, 'plain')


    def _create_html_message(self, alerts, is_dict_type):
        part1 = self._create_text_message(alerts=alerts, is_dict_type=is_dict_type)
        temp = self._load_template(self.html_template_path)
        ARGS_TO_RENDER = self.html_preprocessor(alerts, is_dict_type)
        rendered_content = temp.render(**ARGS_TO_RENDER)
        part2 = MIMEText(rendered_content, 'html')
        msg = MIMEMultipart('alternative')
        msg.attach(part1)
        msg.attach(part2)
        return msg
         


    def list_runtime(self, statuses_to_check):
        alerts = {}
        for status_id in statuses_to_check:
            status_name = None
            if self.get_status_name:
                status_name = self._get_baselinker_status_name(status_id)
            
            status_orders = self._get_baselinker_orders_for_status(status_id)
            
            for status_order in status_orders:
                if self._check_if_order_meets_requirements(status_order):
                    order_fv = None
                    if self.get_invoice:
                        order_fv = self._get_baselinker_invoice_for_order_id(status_order['order_id'])
                    internal_order = self._create_internal_order(status_order, order_fv, status_name)
                    if status_id not in alerts:
                        alerts[status_id] = []
                    if self.dev_limit is not None:
                        if len(alerts[status_id]) >= self.dev_limit:
                            break
                    alerts[status_id].append(internal_order)
        return alerts


    def start(self):

        if self.text_template_path is None:
            raise RuntimeError("Add text template!")

        if isinstance(self.statuses, dict):
            alerts = {}
            for dict_name in self.statuses:
                alerts[dict_name] = self.list_runtime(self.statuses[dict_name])
            if alerts == {}:
                return 
            if self.html_template_path is not None:
                msg_to_send = self._create_html_message(alerts=alerts, is_dict_type=True)
            else:
                msg_to_send = self._create_text_message(alerts=alerts, is_dict_type=True)
            self._send_alert(msg_to_send)
        else:
            alerts = self.list_runtime(self.statuses)
            if alerts == {}:
                return 
            if self.html_template_path is not None:
                msg_to_send = self._create_html_message(alerts=alerts, is_dict_type=False)
            else:
                msg_to_send = self._create_text_message(alerts=alerts, is_dict_type=False)
            self._send_alert(msg_to_send)
            





if __name__ == '__main__':

    czas = datetime.datetime.now() - datetime.timedelta(hours=1)

    t = BaselinkerAlert({"XXX": [125626]}, czas)
    t.smtp_password = "3uzT9zZr4F"
    t.sender = "ALERT: Example"
    t.subject = "Example subject"
    t.recepients = ['johndoe@gmail.com']
    t.get_status_name = True
    t.get_invoice = True

    def pp(x,y):
        print(x)
        return {"items": x['XXX'][125626]}

    t.text_preprocessor = pp

    t.text_template_path = "temp.html"

    t.start()
