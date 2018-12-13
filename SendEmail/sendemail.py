import codecs
import openpyxl
import ConfigParser
import smtplib



config = ConfigParser.ConfigParser()
config.read('configloc.ini')

configpath = config.get('CONFIG','path')

config.read(configpath+"config.ini")

smtpserver = config.get('SMTP','server')
smtpport = config.get('SMTP','port')
smtplogin = config.get('SMTP','login')
smtppassword = config.get('SMTP','password')
            


server = smtplib.SMTP_SSL(smtpserver, smtpport)
server.ehlo()
#Next, log in to the server
server.login(smtplogin, smtppassword)

#ClientSheet = config.get('PROMOTION','ClientSheet')
#ClientSheetFormat = config.get('PROMOTION','ClientSheetFormat')
#promofile = config.get('PROMOTION','file')


def checkvalidity(Sheet):
    ClientSheet = config.get('PROMOTION',Sheet)
    ClientSheetFormat = config.get('PROMOTION',Sheet+'Format')
    promofile = config.get('PROMOTION','file')

    wb = openpyxl.load_workbook(promofile)
    ws = wb[ClientSheet]

    col=0
    ClientSheetFormatFields = ClientSheetFormat.split(',')
    for f in ClientSheetFormatFields:
        col = col + 1
        f1 = f.decode('utf-8').strip()
        if type(ws.cell(row=1, column = col).value) == type(None):
            f2 = ""
        else:
            f2 = ws.cell(row=1, column = col).value.decode('utf-8').strip()
        print f1, f2
        if f1 != f2:
            print ('wrong format')
            server.sendmail("wongkingchung@gmail.com", "wongkingchung@gmail.com", 'wrong format')
            break

    if col == len(ClientSheetFormatFields):            
        print 'right format'

checkvalidity('ClientSheet')
checkvalidity('BVSheet')

##Send the mail
#msg = "Hello!" # The /n separates the message from the headers
#server.sendmail("wongkingchung@gmail.com", "wongkingchung@gmail.com", msg)
