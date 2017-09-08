import time
import urllib2
from urllib2 import urlopen
import pandas as pd
import re
import json

def totaldebt(stock):
    try:
        statssourcecode=urllib2.urlopen('https://finance.yahoo.com/quote/'+stock+'/key-statistics?p='+stock).read()
        totaldebt=float(statssourcecode.split('"totalDebt":{"raw":')[1].split(',')[0])


    except  Exception, e:
        return 0

    return totaldebt


def marketcap(stock):
    try:
        statssourcecode=urllib2.urlopen('https://finance.yahoo.com/quote/'+stock+'/key-statistics?p='+stock).read()
        marketcap=float(statssourcecode.split('"marketCap":{"raw":')[1].split(',')[0])

    except  Exception, e:
        return 0

    return marketcap


def ebit(stock):
    try:

        financialsourcecode=urllib2.urlopen('https://finance.yahoo.com/quote/'+stock+'/financials?p='+stock).read()

        # ebitstr=financialsourcecode.split ('"ebit":{"raw":')[1].split(',')[0]

        p = re.compile('\"ebit\":(.{0,500}),\"operatingIncome')
        m = p.findall(financialsourcecode)
        ret=[]
        for a in m:
            a = '{\"tmp\":' + a + '}'
            b = json.loads(a)
            # print(b['tmp']['raw'], b['endDate']['fmt'])
            ret.append([b['tmp']['raw'], b['endDate']['fmt']])

        # ebit=float(ebitstr.replace(',',''))

    except  Exception, e:

         return [[0,0] for i in range(7)]

    return ret

# def totalpolulation():
#
#     csvfile=pd.read_csv('snp500.csv')
#     return csvfile

def grabebit(population):

     filename=population+'.csv'
     allshares = pd.read_csv(filename)

     allshares['EV/EBIT'] = pd.Series(allshares['Symbol'].size)
     allshares['MV'] = pd.Series(allshares['Symbol'].size)
     allshares['TDebt'] = pd.Series(allshares['Symbol'].size)
     allshares['EBIT'] = pd.Series(allshares['Symbol'].size)

     begintime=time.time()
     i = 0
     for item in allshares['Symbol']:
         try:
             allshares['EV/EBIT'][i]=(marketcap(item)+totaldebt(item))/(ebit(item)[4][0])
         except Exception,e:
             allshares['EV/EBIT'][i]=0

         allshares['MV'][i] = marketcap(item)
         allshares['TDebt'][i] = totaldebt(item)
         try:
             allshares['EBIT'][i]=ebit(item)[4][0]
         except Exception,e:
             allshares['EBIT'][i] = 0

         print allshares['Symbol'][i]
         print allshares['Name'][i]
         print 'EBIT = ',allshares['EBIT'][i]
         print 'EV/EBIT = ', allshares['EV/EBIT'][i]
         print 'Processing ' , time.time()-begintime , 'Seconds'
         i = i + 1
         time.sleep(5)
     allshares.to_csv(population+'results.csv')

if __name__ == '__main__':
    grabebit('russell3000')


