import l_baselinker
import datetime
import l_alerts


STATUSES = [
    125633,
    226603
]

czas = datetime.datetime.now() - datetime.timedelta(hours=24)
t = l_alerts.BaselinkerAlert(STATUSES, czas)


t.smtp_password = "3uzT9zZr4F"
t.sender = "ALERT: Niewysłane zamówienia!"
t.subject = "ALERT: Niewysłane zamówienia w statusie \"Gotowe do wysyłki\""
t.recepients = ['johndoe@gmail.com']
t.get_status_name = True
t.get_invoice = False

def pp(x,y):
    # print(x)
    # exit()
    return {"items": x}

t.text_preprocessor = pp

t.text_template_path = "niewyslaneZamowienia.txt"

t.start()

