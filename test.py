import talib

import database
from utils.util import getKBySymbol, todayStock, removedotBysymbol, getMarketValueBySymbol

#
# database.init()
# data=getKBySymbol('sh.600072')
#
# data=talib.RSI(data['close'])
# print(data)
todayStock()
# code='sh.600000'
# print(removedotBysymbol(code))
# print(getMarketValueBySymbol('sh.600519'))