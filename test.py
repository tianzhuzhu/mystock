import datetime

import pandas as pd
import talib
import baostock as bs
import database
from data.importBasicInformation import queryDubpontByCode, queryGrowthByCode
from utils.util import getKBySymbol, todayStock, removedotBysymbol, getMarketValueBySymbol, getAllMarketValue,  needUpdate

#
# database.init()
# data=getKBySymbol('sh.600072')
#
# data=talib.RSI(data['close'])
# print(data)
# todayStock()
# code='sh.600000'
# print(removedotBysymbol(code))
# print(getMarketValueBySymbol('sh.600519'))
# print(getAllMarketValue())
# bs.login()
# print(queryGrowthByCode('sh.600000'))
updatetime=pd.to_datetime('2021-4-10 11:30:00')
nowtime=pd.to_datetime('2021-4-10 19:30:00')
print((nowtime-updatetime).days)
data=pd.bdate_range(start='2021-4-1 14:00:00' ,periods=40,freq='8H')
data2=pd.bdate_range(start='2021-4-1 14:00:00' ,periods=40,freq='8H')
result=pd.DataFrame()

for i in data:
    for j in data2:
        if(i<=j):
            result.loc[str(i)+''+str(j),['u','n','is']]=[i,j,needUpdate(i,j,True)]

result.to_excel('1.xlsx')

result.columns=['update','now','need']
result.to_excel('2.xlsx')
print(nowtime.hour,updatetime.hour)
print(nowtime.weekday(),updatetime.weekday())

# bs.logout()