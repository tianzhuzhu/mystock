import traceback

import talib
from tqdm import tqdm

import utils.util as util
# way :goldenCross  deathCross
def findMacdListBySymobls(symbols,way='goldenCross',days=100):
    list=[]
    for symbol in tqdm(symbols):
        try:
            tools=util.util()
            data=tools.getKBySymbol(symbol,days)

            # print(data)
            if(len(data.index)<50):
                continue
            data=util.getMacdByData(data)
            # macd:dif macd_signal:dea hist:(dif-dea)*2
            if(way=='goldenCross'):
                if(data.iloc[-2]['macd']<data.iloc[-2]['macd_signal']):
                    if(data.iloc[-1]['macd']>data.iloc[-1]['macd_signal']):
                        # print(data.iloc[-1]['ma10'],data.iloc[-1]['ma30'],data.iloc[-2]['ma10'],data.iloc[-2]['ma30'])
                        list.append(symbol)
            elif(way=='deathCross'):
                if(data.iloc[-2]['macd']>data.iloc[-2]['macd_signal']):
                    if(data.iloc[-1]['macd']<data.iloc[-1]['macd_signal']):
                        # print(data.iloc[-1]['ma10'],data.iloc[-1]['ma30'],data.iloc[-2]['ma10'],data.iloc[-2]['ma30'])
                        list.append(symbol)
                    # print(data)
        except:
            traceback.print_exc()
            pass
    return list
def byMacdMain():
    data=util.todayStock()
    symbols=data['symbol']
    list=findMacdListBySymobls(symbols,'deathCross',days=100)
    return list
if __name__ == '__main__':
    print(byMacdMain())