import talib
import baostock as bs
import database
from data.importBasicInformation import queryDubpontByCode, queryGrowthByCode
from utils.util import getKBySymbol, todayStock, removedotBysymbol, getMarketValueBySymbol, getAllMarketValue

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
bs.login()
print(queryGrowthByCode('sh.600000'))
bs.logout()