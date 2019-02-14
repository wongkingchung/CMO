import codecs
import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



config = ConfigParser.ConfigParser()
config.read('configloc.ini')

configpath = config.get('CONFIG','path')

config.read(configpath+"config.ini")


smtpserver = config.get('SMTP','server')
smtpport = config.get('SMTP','port')
smtplogin = config.get('SMTP','login')
smtppassword = config.get('SMTP','password')
receiver = config.get('SMTP','receiver')
sender = config.get('SMTP','sender')            
subject = config.get('SMTP','subject')


def sendmail(body):

    server = smtplib.SMTP(smtpserver, smtpport)
##    server.ehlo()
    server.login(smtplogin, smtppassword)
     
    msg = MIMEMultipart() ##//used for define multipart message
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject']= subject
     
##    body = 'hi everyone ! this email is from python'
    msg.attach(MIMEText(body, 'plain'))  ##// attach body to the message, here email is plain so email type plain is used
    text = msg.as_string()  ##// used for converting object into plain text string
    
    server.sendmail(sender, receiver, text)

##sendmail('this is a test3')
