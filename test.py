import talib

import database
from utils.util import getKBySymbol

database.init()
data=getKBySymbol('sh.600072')

data=talib.RSI(data['close'])
print(data)