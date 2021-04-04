import traceback

import stockstats
from tqdm import tqdm

from utils import util


def findCRBySymbols(symbols,days=100):
    for symbol in tqdm(symbols):
        try:
            tools=util.util()
            data=tools.getKBySymbol(symbol,days)
            stockdata=stockstats.StockDataFrame.retype(data)
            stockdata.get('macd')
            print(stockdata['cr'])

        except:
            traceback.print_exc()
def byCRMain():
    data=util.todayStockData()
    symbols=data['symbol']
    list=findCRBySymbols(symbols)
    return list
if __name__ == '__main__':
    print(byCRMain())