import urllib2
import json

import codecs
import pyodbc
import ConfigParser

import os
import shutil
import datetime
import re

minv = ''
maxv = ''

config = ConfigParser.ConfigParser()
config.read('configloc.ini')

configpath = config.get('CONFIG','path')

config.read(configpath+"config.ini")


server = config.get('DB','server')
database = config.get('DB','database')
username = config.get('DB','username')
password = config.get('DB','password')


driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password+';Charset=UTF8')
cursor = cnxn.cursor()


req = urllib2.Request("https://appws.convoy.com.hk/vsmartClientConsultantAPI/GetJson.svc/LifeInsuranceProductBasicPlan?sid=cv1tiasd3l5md8kw")
opener = urllib2.build_opener()
f = opener.open(req)
records = json.loads(f.read())

SQLCommand = "truncate table icompare.import_vsmart_bv_sorting"
cursor.execute(SQLCommand)
 
for record in records:
##    print record['ProviderCode'], record['Internal Code']
##    SQLCommand = u"INSERT INTO icompare.vsmart_LifeInsuranceProductBasicPlanForiCompare (ProviderCode, InternalCode, AlternatedSchemeProductCode, ProductType, SubCategory, Provider, GeneralName, StatementName,termtype, termpaymentinyear, termpaymentinmonth, tier,installment,installmentyear,bvfactor,effectivefrom,effectiveto) VALUES ('" +record['ProviderCode'] + "','"+record['Internal Code'] + "','"+record['Product Type'] + "','"+ record['SubCategory'] +"','"+ record['Provider']+"','"+ record['General Name'] + "','"+ record['Statement Name'] + "','"+ record['Term Type'] + "','"+record['Term Payment In Year'] +"','"+record['Term Payment In Month'] + "','" + record['Tier'] + "','" + record['Installment'] + "'," + str(record['InstallmentYear']) + ","+ str(record['BV Factor']) +",'"+record['Effective From']+"','"+record['Effective To']+ "');" 
    SQLCommand = "INSERT INTO icompare.import_vsmart_bv_sorting (id, installment, payterm, agemin, agemax, ccy, bvfactor, eff_from, eff_to, generalname,termtype, tier, productleveleffdate, prc) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)"


##    minage = 0
##    maxage = 999
    minv = 0
    maxv = 999
    ccy ='ANY'
    
    found = re.search(r'\bage(\d{1,3}\b)\s*?-\s*?(\b\d{1,3}\b)',record['Tier'], re.I)
    rule=10
    if not (found):
        found = re.search(r'((?<![\d.,])[0-9]{1,3}(?![\d.,]))\s*-\s*((?<![\d.])[0-9]{1,3}(?![\d.]))',record['Tier'],re.I)
        rule =20
        if not(found):
                found = re.search(r'age (below|above)\s+(\d{1,3})',record['Tier'],re.I)
                rule = 25
                if not(found):
                    found = re.search(r'age.*?([=><]+).*?(\d+)',record['Tier'], re.I)
                    rule =30
                    if not(found):
                        found = re.search(r'([=><]+).?age.*?(\d+)',record['Tier'], re.I)
                        rule =40
                        if not(found):
                            found = re.search(r'[^.,](\b\d{1,2}\b)[^0-9]*(above|below)',record['Tier'], re.I)
                            rule =50
                            if not(found):
                                found = re.search(r'(\b\d{1,2}\b).*?(below|above)', record['Tier'], re.I)
                                rule = 60
                                if not(found):
                                    found = re.search(r'(above|below)\s*(\b\d{1,2}\b)', record['Tier'], re.I)
                                    rule=70
                                    if not(found):
                                         found = re.search(r'(age)\s*(\b\d{1,2}\b)',record['Tier'], re.I)
                                         rule =80
                                         if not(found):
                                             found = re.search(r'()\A(\d{2})\Z',record['Tier'],re.I)
                                             rule = 90
                                
                                      
                                                  
    if found:
        minv = found.group(1)
        maxv = found.group(2)
        if minv == ">" or minv == '>=' or minv.lower() =='above':
            minv = maxv
            maxv = '999'
        if minv == '<' or minv == '<=' or minv.lower() == 'below':
             minv = '0'

        if maxv == ">" or maxv == '>=' or maxv.lower() =='above':
            maxv = '999'
        if maxv == '<' or maxv == '<=' or maxv.lower() == 'below':
            maxv = minv
            minv = '0'

        if minv == 'age' or minv == 'Age' or minv=='':
            minv = maxv

    else:
        found = re.search(r'(HKD|USD|RMB)',record['Tier'], re.I)
        rule = 100
        if found:
            ccy = found.group(1)
 
    minage = minv
    maxage = maxv

    payterm = record['Term Payment In Year']
    if record['Term Type'] == 'Age':
        payterm = int(record['Term Max Age']) * -1
    if record['Term Type'] == '':
        payterm = 0

    print record['Internal Code'], record['InstallmentYear'],payterm, minage, maxage, ccy
    cursor.execute(SQLCommand, record['Internal Code'], record['InstallmentYear'],payterm, minage, maxage, ccy,record['BV Factor'] , record['Effective From'],record['Effective To'], record['General Name'], record['Term Type'], record['Tier'], record['Product Level Effective Date'], record['Available for PRC Client'])

cnxn.commit()


##
##req = urllib2.Request("https://appws.convoy.com.hk/vsmartClientConsultantAPI/GetJson.svc/LifeInsuranceProductRider?sid=cv1tiasd3l5md8kw")
##opener = urllib2.build_opener()
##f = opener.open(req)
##records = json.loads(f.read())
##
##SQLCommand = "truncate table icompare.vsmart_LifeInsuranceProductRiderForiCompare"
##cursor.execute(SQLCommand)
## 
##for record in records:
##    SQLCommand = "INSERT INTO icompare.vsmart_LifeInsuranceProductRiderForiCompare (ProviderCode, InternalCode,Category, GeneralName,StatementName,AlternatedSchemeProductCode,Scheme,RiderFollowBasicPlan,RiderType,Tier,Installment,InstallmentYear,Promotion,ProductID,VariantId, Term, BVFactor, EffectiveFrom, EffectiveTo, TermType, TermPaymentInYear, TermMaxAge) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
##    cursor.execute(SQLCommand, record['ProviderCode'],record['Internal Code'],record['Category'], record['General Name'], record['Statement Name'], record['Alternated Scheme Product Code'], record['Scheme'],record['Rider Follow Basic Plan'],record['Rider Type'],record['Tier'],record['Installment'], record['InstallmentYear'], record['Promotion'],record['ProductID'],record['Variant Id'], record['Term'], record['BV Factor'], record['Effective From'],record['Effective To'], record['Term Type'],record['Term Payment In Year'], record['Term Max Age'])
##cnxn.commit()


##
##req = urllib2.Request("https://appws.convoy.com.hk/vsmartClientConsultantAPI/GetJson.svc/LifeInsuranceProductBasicRiderRelationship?sid=cv1tiasd3l5md8kw")
##opener = urllib2.build_opener()
##f = opener.open(req)
##records = json.loads(f.read())
##
##SQLCommand = "truncate table icompare.vsmart_LifeInsuranceProductBasicRiderRelationshipForiCompare"
##cursor.execute(SQLCommand)
## 
##for record in records:
##    SQLCommand = "INSERT INTO icompare.vsmart_LifeInsuranceProductBasicRiderRelationshipForiCompare (RiderProviderCode, RiderProductID, RiderInternalCode,RiderAlternatedSchemeProductCode,RiderScheme,BasicPlanProviderCode,BasicPlanProductID,BasicPlanInternalCode,BasicPlanScheme) VALUES (?,?,?,?,?,?,?,?,?)"
##    cursor.execute(SQLCommand, record['Rider ProviderCode'], record['Rider ProductID'],record['Rider Internal Code'], record['Rider Alternated Scheme Product Code'], record['Rider Scheme'],record['BasicPlan ProviderCode'], record['BasicPlan ProductID'], record['BasicPlan Internal Code'], record['BasicPlan Scheme'])
##cnxn.commit()

