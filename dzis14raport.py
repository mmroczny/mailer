from jinja2.environment import Template
import l_baselinker
import datetime
import l_alerts

CONFIGS = {
    "ap": [125623],
    "ip": [226602]
}


dzis_14 = datetime.datetime.now()
dzis_14 = dzis_14.replace(hour=14, minute=15, second=0, microsecond=0)
t = l_alerts.BaselinkerAlert(CONFIGS, dzis_14)


t.smtp_password = "3uzT9zZr4F"
t.sender = "ALERT: Niespakowane zamówienia!"
t.subject = "ALERT: Niespakowane zamówienia w statusie \"Przekazano do realizacji\"!"
t.recepients = ['johndoe@gmail.com']
t.get_status_name = True
t.get_invoice = True

def pp(x,y):
    results = {}
    for hurt in x:
        results[hurt] = {"s":[], "r": [], "p": []}
        for status in x[hurt]:
            for order in x[hurt][status]:
                if '-S' in order['fv']:
                    results[hurt]['s'].append(order)
                elif '-R' in order['fv']:
                    results[hurt]['r'].append(order)
                else:
                    results[hurt]['p'].append(order)
    
    
    return results

t.text_preprocessor = pp
t.html_preprocessor = pp

t.text_template_path = "dzis14raport.txt"
t.html_template_path = "dzis14raport.html"

t.dev_limit = 3

t.start()


