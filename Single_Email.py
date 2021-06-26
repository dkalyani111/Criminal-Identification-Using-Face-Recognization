#for single email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
from datetime import timedelta
import mysql.connector as con



s = smtplib.SMTP(host='smtp.gmail.com', port=587) #simple mail tranfer protocall
s.starttls()
s.login("testingprojects2019@gmail.com", "Testing123@")





msg = MIMEMultipart()      


msg['From']="testingprojects2019@gmail.com"

msg['Subject']="Mail Smart Criminal Detection System"
def send_email(to_mail,msgs):
    
    msg['To']=to_mail
    msg.attach(MIMEText(msgs, 'plain'))
    s.send_message(msg)

