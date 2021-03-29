import pandas as pd
import pandas_datareader as web
from datetime import datetime, timedelta
import talib
import matplotlib as mpl# 用于设置曲线参数
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.ticker as ticker
import mplfinance as mpf
import numpy as np
from sqlalchemy import create_engine
def stock(stock_code): #stock_code是股票代码，例子：上市 "600036.ss", 深市 "000001.sz"
    start_date = "2020-12-01"  #起始日期
    today = datetime.date(datetime.now())  #截止日期
    stock_info = web.get_data_yahoo(stock_code, start_date, today)  #获取行情数据，返回dataframe
    stock_info = stock_info.reset_index()  #默认index是日期，这里要重置一下，为后面绘图做准备
    stock_info = stock_info.astype({"Date": str})    #将Date列的类型设置为str，为绘图做准备
    print(stock_info.columns)
    return stock_info
def query(code,days):
    daydelay=50
    sql="	SELECT date, open, high,close,low ,volume from tb_stock_hisotry_detatil WHERE code ='{}' ORDER BY date desc limit 0,{}".format(code,days+daydelay)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    data = pd.read_sql(sql,engine)
    data.rename(columns={'date':'Date', 'open':'Open', 'high':'High','close':'Close','low':'Low' ,'volume':'Volume'},inplace=True)
    data.set_index('Date',inplace=True)
    data=pd.DataFrame(data,dtype=float)
    data.sort_index(inplace=True, ascending=True)
    data.reset_index(inplace=True)
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])
    # 获取10日均线和30日均线
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)
    # 获取rsi
    data["rsi"] = talib.RSI(data["Close"])
    data=pd.DataFrame(data.iloc[daydelay:daydelay+days])
    data.reset_index(inplace=True)
    data.drop(columns='index',inplace=True)
    data['Date']=pd.to_datetime(data['Date'])
    data.set_index('Date',inplace=True)
    return data
def get_indicators(stock_code):
    # 创建dataframe

    data = stock(stock_code)

    #获取macd
    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])

    #获取10日均线和30日均线
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)

    #获取rsi
    data["rsi"] = talib.RSI(data["Close"])
    return data
def plot_chart(data, title):
    fig = plt.figure()  # 创建绘图区，包含四个子图
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.72, 1, 0.32))  # 蜡烛图子图
    mpf.plot(data, type='candle', figscale=0.9,ax=ax_candle)
    fig.savefig('1.jpg')

def industry(dict):
    np.seterr(divide='ignore', invalid='ignore') # 忽略warning
    for key, value in dict.items():
        # d.iteritems: an iterator over the (key, value) items
        stock_info = get_indicators(key)
        plot_chart(stock_info, value)
def industryFromSQL(list):
    # np.seterr(divide='ignore', invalid='ignore')  # 忽略warning
    for i in list:
        data=query(i,100)
        print('finshed querry')
        print(data)
        # data=get_indicators(data)
        plot_chart(data,i)


if __name__=='__main__':
    # finance_list = {
    #     "600036.ss": "Zhaoshang Yinhang",
    #     # "002142.sz": "Ningbo Yinhang",
    #     # "000001.sz": "Pingan Yinhang",
    #     # "601318.ss": "Zhongguo Pingan"
    # }
    # industry(finance_list)
    list=['sh.601398']
    industryFromSQL(list)

