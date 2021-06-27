import datetime
import l_alerts

DEFAULT_SENDER = "Oczekujące zamówienia! <johndoe@gmail.com>"

# #Poniższe zamówienia są w statusach ponad 2h
#     msg["Subject"] = "ALERT: Oczekujące zamówienia w statusie \"Zapłacone / Pobranie\"!"


STATUSES = [
    125626,
    161533,
    250882,
    253070,
    144108,
    162884,
    233533,
    216735,
    252528,
    260135,
    260136,
]


czas = datetime.datetime.now() - datetime.timedelta(hours=6)
t = l_alerts.BaselinkerAlert(STATUSES, czas)


t.smtp_password = "3uzT9zZr4F"
t.sender = "ALERT: Oczekujące zamówienia!"
t.subject = "ALERT: Oczekujące zamówienia w statusie \"Zapłacone / Pobranie\"!"
t.recepients = ['johndoe@gmail.com']
t.get_status_name = True
t.get_invoice = False

def pp(x,y):
    # print(x)
    # exit()
    return {"items": x}

t.text_preprocessor = pp

t.text_template_path = "oplaconeBrakRealizacji.txt"

t.start()