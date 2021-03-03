import RPi.GPIO as GPIO
import sys
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3 as lite

#kütüphanelerimi ekledim

con = lite.connect("alarm")
cur = con.cursor()


GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
GPIO.setup(18,GPIO.OUT)

#GPIO pinlerime bağladığım kablolarımı burada tanımladım


def sendMail():
    message = MIMEMultipart()
    message["From"] = "uygulamamaili1@gmail.com"
    message["To"] = "beyzam1d@gmail.com"
    message["Subject"] = "HAREKET TESPIT EDILDI!"

    body = """
    SUPHELI HAREKET TESPIT EDILDI!!! LUTFEN KAPINIZI KONTROL EDIN!!!

    """
    body = body + str(datetime.datetime.now())
    body_text = MIMEText(body,"plain")
    message.attach(body_text)

#mail içeriğini burada belirttim

  try:
        mail = smtplib.SMTP("smtp.gmail.com",587)
        mail.ehlo()
        mail.starttls()
        mail.login("XX@gmail.com","ŞİFRENİZ")
        mail.sendmail(message["From"],message["To"],message.as_string())
        mail.close()
        print("MAIL GONDERILDI")
    except:
        print("MAIL GONDERILEMEDI!")

#mailimi burada tanıttım SMTP metodunu kullandım

def insert():
    Insert = [(datetime.datetime.now())]
    cur.execute('''INSERT INTO alarm (date) VALUES (?)''',Insert)
    con.commit()
    print("Insert Success!")

#datetime.now metodu mailime hareketin algılandığı anda gönderilmesini sağlayacak

try:
    while True:
        if GPIO.input(23):
            print("HAREKET VAR!!")
            insert()
            sendMail()
            GPIO.output(18,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(18,GPIO.LOW)
except KeyboardInterrupt:
    GPIO.cleanup()
    con.close()