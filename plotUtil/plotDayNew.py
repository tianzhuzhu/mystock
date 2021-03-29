import pandas as pd
import pandas_datareader as web
from datetime import datetime, timedelta
import talib
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
    sql="SELECT date,high,low ,open,close,volume from tb_stock_hisotry_detatil WHERE code ='{}' ORDER BY date desc limit 0,{}".format(code,days+daydelay)
    print(sql)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    data = pd.read_sql(sql,engine)
    print(data)
    data.rename(columns={'date':'Date', 'open':'Open', 'high':'High','close':'Close','low':'Low' ,'volume':'Volume'},inplace=True)
    data.set_index('Date',inplace=True)
    print(data)
    data=pd.DataFrame(data,dtype=float)
    data.sort_index(inplace=True, ascending=True)

    data.reset_index(inplace=True)

    data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'])
    # 获取10日均线和30日均线
    data["ma10"] = talib.MA(data["Close"], timeperiod=10)
    data["ma30"] = talib.MA(data["Close"], timeperiod=30)
    # 获取rsi
    data["rsi"] = talib.RSI(data["Close"])


    data['K'], data['D'] = talib.STOCH(data.High.values, data.Low.values,
                                                       data.Close.values, \
                                                       fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3,
                                                       slowd_matype=0)

    data['J'] = 3 * data['K'] - 2 * data['D']

    data = data.iloc[daydelay:daydelay + days]
    data.reset_index(inplace=True)
    data.drop(columns='index',inplace=True)
    print(data)
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

def plot_chart(outputpath,data, title):
    data.to_excel(title+'.xlsx')
    print(data)
    fig = plt.figure()  #创建绘图区，包含四个子图
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.75, 1, 0.25))   #蜡烛图子图
    # left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax_macd = fig.add_axes((0, 0.60, 1, 0.15), sharex=ax_candle)  #macd子图
    ax_rsi = fig.add_axes((0, 0.45, 1, 0.15), sharex=ax_candle)  #rsi子图
    ax_vol = fig.add_axes((0, 0.30, 1, 0.15), sharex=ax_candle)   #成交量子图
    ax_kjd = fig.add_axes((0, 0.15, 1,0.15), sharex=ax_candle)
    ax_candle.grid(True)
    # ax_macd.grid(True)
    # ax_rsi.grid(True)
    # ax_vol.grid(True)
    # ax_kjd.grid(True)
    # print(data)
    ohlc = []   #存放行情数据，candlestick_ohlc需要传入固定格式的数据
    row_number = 0
    for date, row in data.iterrows():
        date, highp, lowp, openp, closep = row[:5]
        ohlc.append([row_number, openp, highp, lowp, closep])
        row_number = row_number+1
    # print(ohlc)
    date_tickers = data.Date.values #获取Date数据
    # print(date_tickers)
    #绘制蜡烛图

    candlestick_ohlc(ax_candle, ohlc
    , colorup = "r", colordown = "g"
    )
    def format_date(x, pos=None):
        # 由于前面股票数据在 date 这个位置传入的都是int
        # 因此 x=0,1,2,...
        # date_tickers 是所有日期的字符串形式列表
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        return date_tickers[int(x)]

    # ax_candle = fig.add_axes((0, 0.75, 1, 0.25))  # 蜡烛图子图
    # stockData=data.copy()
    # stockData['Date'] = pd.to_datetime(stockData['Date'])
    # stockData.set_index('Date',inplace=True)
    # mpf.plot(stockData, type='candle', figscale=0.9,ax=ax_candle)
    ax_candle.plot(data.index, data["ma10"], label="MA10")
    ax_candle.plot(data.index, data["ma30"], label="MA30")
    ax_candle.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    ax_candle.xaxis.set_major_locator(ticker.MultipleLocator(2))  # 设置间隔为6个交易日

    ax_candle.grid(True)
    ax_candle.set_title(title, fontsize=20)
    ax_candle.legend()

    for label in ax_kjd.xaxis.get_ticklabels():
        label.set_rotation(60)


    # 绘制MACD
    ax_macd.plot(data.index, data["macd"], label="macd")
    ax_macd.bar(data.index, data["macd_hist"] * 3, label="hist")
    ax_macd.plot(data.index, data["macd_signal"], label="signal")
    ax_macd.set_title('MACD')
    ax_macd.legend()

    #绘制RSI
    ax_rsi.set_ylabel("(%)")
    ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
    ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
    ax_rsi.plot(data.index, data["rsi"], label="rsi")
    ax_rsi.set_title('RSI')
    ax_rsi.legend()

    #绘制成交量
    ax_vol.bar(data.index, data["Volume"] / 1000000)
    ax_vol.set_ylabel("(Million)")



    #KDJ
    ax_kjd.plot(data.index, data["K"],label="K",color='blue')
    ax_kjd.plot(data.index, data["D"], label="D",color='g')
    ax_kjd.plot(data.index, data["J"], label="J",color='r')
    ax_kjd.set_title('KDJ')
    # graph_KDJ.plot(np.arange(0, len(figData.index)), figData['K'], 'blue', label='K')  # K
    # graph_KDJ.plot(np.arange(0, len(figData.index)), figData['D'], 'g--', label='D')  # D
    # graph_KDJ.plot(np.arange(0, len(figData.index)), figData['J'], 'r-', label='J')  # J
    ax_kjd.legend()
    #这里个人选择不要plt.show()，因为保存图片到本地的
    #plt.show()
    # 保存图片到本地
    fig.savefig(outputpath, bbox_inches="tight")
    return outputpath

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
def plotK(path,title,code):
    data=query(code,100)
    print('finshed querry')
    print(data)
    # data=get_indicators(data)
    path=plot_chart(path,data,title)
    return path
if __name__=='__main__':
    # finance_list = {
    #     "600036.ss": "Zhaoshang Yinhang",
    #     # "002142.sz": "Ningbo Yinhang",
    #     # "000001.sz": "Pingan Yinhang",
    #     # "601318.ss": "Zhongguo Pingan"
    # }
    # industry(finance_list)
    path='sh.600007'+'.jpg'
    list=['sh.601398']
    plotK('sh.600007'+'.jpg','sh.600007','sh.600007')

