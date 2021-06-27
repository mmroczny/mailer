import datetime
import l_alerts


STATUSES = [
    226602,
    125623,
]


czas = datetime.datetime.now() - datetime.timedelta(hours=48)
t = l_alerts.BaselinkerAlert(STATUSES, czas)


t.smtp_password = "3uzT9zZr4F"
t.sender = "ALERT: Przekazane do realizacji!"
t.subject = "ALERT: Przekazane do realizacji 48h!"
t.recepients = ['johndoe@gmail.coml']
t.get_status_name = True
t.get_invoice = False

def pp(x,y):
    
    return {"items": x}

t.text_preprocessor = pp

t.text_template_path = "oplaconeBrakRealizacji.txt"

t.start()