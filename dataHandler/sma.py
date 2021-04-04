import traceback

import talib
from tqdm import tqdm

import utils.util as util
# way :goldenCross  deathCross
def findSMAbySymbols(symbols,way='goldenCross',fast=5,slow=10,days=100):
    list=[]
    for symbol in tqdm(symbols):
        fastName='ma'+str(fast)
        slowName='ma'+str(slow)
        try:
            tools=util.util()
            data=tools.getKBySymbol(symbol,days)
            if(len(data.index)<50):
                continue
            data=util.getMaBydata(data,[fast,slow])
            if(way=='goldenCross'):
                if(data.iloc[-2][fastName]<data.iloc[-2][slowName]):
                    if(data.iloc[-1][fastName]>data.iloc[-1][slowName]):
                        list.append(symbol)
            elif(way=='deathCross'):
                if(data.iloc[-2][fastName]>data.iloc[-2][slowName]):
                    if(data.iloc[-1][fastName]<data.iloc[-1][slowName]):
                        list.append(symbol)
        except:
            traceback.print_exc()
            pass
    return list
def bySMAMain():
    data=util.todayStockData()
    symbols=data['symbol']
    list=findSMAbySymbols(symbols,'deathCross')
    return list
if __name__ == '__main__':
    print(bySMAMain())