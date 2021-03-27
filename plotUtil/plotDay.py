import datetime
import os

import talib
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf

import utils.loadData

np.seterr(divide='ignore',invalid='ignore') # 忽略warning
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
fig = plt.figure(figsize=(20,12), dpi=100,facecolor="white") #创建fig对象
from sqlalchemy import create_engine
def query(code,days):
    sql="	SELECT code, date, open, high,close,low ,volume from tb_stock_hisotry_detatil WHERE code ='{}' ORDER BY date desc limit 0,{}".format(code,days)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    data = pd.read_sql(sql,engine)
    return data
def queryName(code):
    sql="	SELECT name from todaystock WHERE code ='{}' ".format(code)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    data = pd.read_sql(sql,engine)
    return data.iloc[0,0]
def plot_k(outputPath,ts_code,title):
    print('绘图',ts_code)
    name=queryName(ts_code[3:])+'-'+title
    days=200
    # y_color = mpf.make_marketcolors(up='red',  # 上涨时为红色
    #                                 down='green',  # 下跌时为绿色
    #                                 edge='i',  # 隐藏k线边缘
    #                                 volume='in',  # 成交量用同样的颜色
    #                                 inherit=True)

    df_stockload = query(ts_code,days=days)
    df_stockload.rename(columns={'volume':'vol','date':'trade_date'},inplace=True)
    # df_stockload.rename(columns={'volume':'volume','date':'Date','open':'opene','close':'close','high': 'high', 'low': 'low'},inplace=True)
    df_stockload.drop(columns=['code'],inplace=True)
    df_stockload['trade_date'] = pd.to_datetime(df_stockload['trade_date'])
    df_stockload=df_stockload.set_index('trade_date')
    df_stockload=pd.DataFrame(df_stockload,dtype=float)
    df_stockload.sort_index(inplace=True,ascending=True)
    print(df_stockload.dtypes)


    gs = gridspec.GridSpec(4, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1.5,1.5,1.5])
    graph_KAV = fig.add_subplot(gs[0,:])
    graph_VOL = fig.add_subplot(gs[1,:])
    graph_MACD = fig.add_subplot(gs[2,:])
    graph_KDJ = fig.add_subplot(gs[3,:])

    print(df_stockload)
    #绘制K线图
    t=100
    n=days-t
    figData=df_stockload.iloc[n:days].copy()
    mpf.candlestick2_ochl(graph_KAV, figData.open, figData.close, figData.high, figData.low, width=0.5,
                          colorup='r', colordown='g')  # 绘制K线走势
    # graph_KAV=mpf.plot(figData)
    #绘制移动平均线图
    print(df_stockload.close.rolling(window=5).mean())
    figData['Ma5'] = (df_stockload.close.rolling(window=5).mean().copy()).iloc[n:days]#pd.rolling_mean(df_stockload.close,window=20)
    figData['Ma10'] = (df_stockload.close.rolling(window=10).mean()).copy().iloc[n:days]#pd.rolling_mean(df_stockload.close,window=30)
    figData['Ma20'] = (df_stockload.close.rolling(window=20).mean().copy()).iloc[n:days]#pd.rolling_mean(df_stockload.close,window=60)
    # df_stockload['Ma30'] = df_stockload.close.rolling(window=30).mean()#pd.rolling_mean(df_stockload.close,window=60)
    # df_stockload['Ma60'] = df_stockload.close.rolling(window=60).mean()#pd.rolling_mean(df_stockload.close,window=60)
    print(figData['Ma5'])
    graph_KAV.plot(np.arange(0, len(figData.index)), figData['Ma5'],'black', label='M5',lw=1.0)
    graph_KAV.plot(np.arange(0, len(figData.index)), figData['Ma10'],'green',label='M10', lw=1.0)
    graph_KAV.plot(np.arange(0, len(figData.index)), figData['Ma20'],'blue',label='M20', lw=1.0)
    # graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma30'],'pink', label='M30',lw=1.0)
    # graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma60'],'yellow',label='M60', lw=1.0)

    # 添加网格
    graph_KAV.grid()
    # graph_KAV.set_title(ts_code + '-' + name,fontsize=10)
    graph_KAV.legend(loc='best')

    graph_KAV.set_ylabel=u"价格"
    graph_KAV.set_xlim(0, len(figData.index))  # 设置一下x轴的范围

    graph_VOL.bar(np.arange(0, len(figData.index)), figData.vol,color=['g' if figData.open[x] > figData.close[x] else 'r' for x in range(0,len(figData.index))])
    graph_VOL.set_ylabel(u"成交量")
    graph_VOL.set_xlim(0,len(figData.index)) #设置一下x轴的范围
    graph_VOL.set_xticks(range(0,len(figData.index),15))#X轴刻度设定 每15天标一个日期

    macd_dif, macd_dea, macd_bar = talib.MACD(df_stockload['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_dif, macd_dea, macd_bar=macd_dif[n:days],macd_dea[n:days],macd_bar[n:days]

    graph_MACD.plot(np.arange(0, len(figData.index)), macd_dif, 'red', label='macd dif')  # dif
    graph_MACD.plot(np.arange(0, len(figData.index)), macd_dea, 'blue', label='macd dea')  # dea

    bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)# 绘制BAR>0 柱状图
    bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)# 绘制BAR<0 柱状图
    graph_MACD.bar(np.arange(0, len(figData.index)), bar_red, facecolor='red')
    graph_MACD.bar(np.arange(0, len(figData.index)), bar_green, facecolor='green')

    graph_MACD.legend(loc='best',shadow=True, fontsize ='10')
    graph_MACD.set_ylabel(u"MACD")
    graph_MACD.set_xlim(0,len(figData.index)) #设置一下x轴的范围
    graph_MACD.set_xticks(range(0,len(figData.index),15))#X轴刻度设定

    #绘制KDJ
    df_stockload['K'], df_stockload['D'] = talib.STOCH(df_stockload.high.values, df_stockload.low.values, df_stockload.close.values, \
                                                       fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    df_stockload['J'] = 3 * df_stockload['K'] - 2 * df_stockload['D']
    figData['K']=df_stockload['K'].iloc[n:days]
    figData['D']=df_stockload['D'].iloc[n:days]
    figData['J']=df_stockload['J'].iloc[n:days]


    graph_KDJ.plot(np.arange(0, len(figData.index)), figData['K'], 'blue', label='K')  # K
    graph_KDJ.plot(np.arange(0, len(figData.index)), figData['D'], 'g--', label='D')  # D
    graph_KDJ.plot(np.arange(0, len(figData.index)), figData['J'], 'r-', label='J')  # J
    graph_KDJ.legend(loc='best', shadow=True, fontsize='10')

    graph_KDJ.set_ylabel(u"KDJ")
    graph_KDJ.set_xlabel("日期")
    graph_KDJ.set_xlim(0, len(figData.index))  # 设置一下x轴的范围
    graph_KDJ.set_xticks(range(0, len(figData.index), 15))  # X轴刻度设定 每15天标一个日期
    graph_KDJ.set_xticklabels(
        [figData.index.strftime('%Y-%m-%d')[index] for index in graph_KDJ.get_xticks()])  # 标签设置为日期

    # X-轴每个ticker标签都向右倾斜45度
    for label in graph_KAV.xaxis.get_ticklabels():
        label.set_visible(False)

    for label in graph_VOL.xaxis.get_ticklabels():
        label.set_visible(False)

    for label in graph_MACD.xaxis.get_ticklabels():
        label.set_visible(False)

    for label in graph_KDJ.xaxis.get_ticklabels():
        label.set_rotation(45)
    label.set_fontsize(10)  # 设置标签字体
    plt.savefig(outputPath)
    print(outputPath)

    plt.cla()
    graph_MACD.remove()
    graph_KAV.remove()
    graph_VOL.remove()
    graph_KDJ.remove()
    return outputPath
if __name__=='__main__':
    # ouputpath=utils.loadData.loadData('config.yml')['path']['default-kLine']
    # date=datetime.datetime.now().date()
    #
    # path=os.path.join(ouputpath,str(date))
    # if(not os.path.exists(path)):
    #     os.mkdir(path)
    path='sh.600007'+'.jpg'
    # print(path)
    plot_k(path,ts_code='sh.600007',title='日线')
    # path = 'sh.600006' + '.jpg'
    # plot_k(path,ts_code='sh.600006',title='日线')