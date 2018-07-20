import codecs
import pyodbc
server = 'dtdlive.database.windows.net'
database = 'imsure'
username = 'imsure'
password = 'JKn_sa89Dm'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("SELECT TOP 20  title from icompare.article")
row = cursor.fetchone()
with codecs.open("C:\Coding\python\ETL\output.csv","a",encoding="utf8") as d:
    while row:
        print str(row).decode('unicode-escape')
        d.write(str(row).decode('unicode-escape') +"\n")
        row = cursor.fetchone()
