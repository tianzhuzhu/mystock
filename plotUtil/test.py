import talib
import numpy as np
import psycopg2 as pg
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec#分割子图
import mpl_finance as mpf
np.seterr(divide='ignore',invalid='ignore') # 忽略warning
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
fig = plt.figure(figsize=(30,16), dpi=100,facecolor="white") #创建fig对象
from sqlalchemy import create_engine
def query(code,days):
    sql="	SELECT code, date, open, high,close,low ,volume from tb_stock_hisotry_detatil WHERE code ='{}' ORDER BY date desc limit 0,{}".format(code,days)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    data = pd.read_sql(sql,engine)
    return data

ts_code = 'SZ.000001' #股票代码
name = '平安银行'
df_stockload = query(ts_code,days=100)
df_stockload.rename(columns={'volume':'vol','date':'trade_date'},inplace=True)
df_stockload.drop(columns=['code'],inplace=True)
df_stockload['trade_date'] = pd.to_datetime(df_stockload['trade_date'])
df_stockload=df_stockload.set_index('trade_date')
df_stockload=pd.DataFrame(df_stockload,dtype=float)
print(df_stockload.dtypes)
gs = gridspec.GridSpec(4, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0, height_ratios=[3.5,1,1,1])
graph_KAV = fig.add_subplot(gs[0,:])
graph_VOL = fig.add_subplot(gs[1,:])
graph_MACD = fig.add_subplot(gs[2,:])
graph_KDJ = fig.add_subplot(gs[3,:])

print(df_stockload)
#绘制K线图
mpf.candlestick2_ochl(graph_KAV, df_stockload.open, df_stockload.close, df_stockload.high, df_stockload.low, width=0.5,
                      colorup='r', colordown='g')  # 绘制K线走势

#绘制移动平均线图
df_stockload['Ma5'] = df_stockload.close.rolling(window=5).mean()#pd.rolling_mean(df_stockload.close,window=20)
df_stockload['Ma10'] = df_stockload.close.rolling(window=10).mean()#pd.rolling_mean(df_stockload.close,window=30)
df_stockload['Ma20'] = df_stockload.close.rolling(window=20).mean()#pd.rolling_mean(df_stockload.close,window=60)
df_stockload['Ma30'] = df_stockload.close.rolling(window=30).mean()#pd.rolling_mean(df_stockload.close,window=60)
df_stockload['Ma60'] = df_stockload.close.rolling(window=60).mean()#pd.rolling_mean(df_stockload.close,window=60)

graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma5'],'black', label='M5',lw=1.0)
graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma10'],'green',label='M10', lw=1.0)
graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma20'],'blue',label='M20', lw=1.0)
graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma30'],'pink', label='M30',lw=1.0)
graph_KAV.plot(np.arange(0, len(df_stockload.index)), df_stockload['Ma60'],'yellow',label='M60', lw=1.0)

# 添加网格
graph_KAV.grid()

graph_KAV.legend(loc='best')
graph_KAV.set_title(ts_code + ' ' + name)
graph_KAV.set_ylabel(u"价格")
graph_KAV.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围

graph_VOL.bar(np.arange(0, len(df_stockload.index)), df_stockload.vol,color=['g' if df_stockload.open[x] > df_stockload.close[x] else 'r' for x in range(0,len(df_stockload.index))])
graph_VOL.set_ylabel(u"成交量")
graph_VOL.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_VOL.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定 每15天标一个日期

macd_dif, macd_dea, macd_bar = talib.MACD(df_stockload['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dif, 'red', label='macd dif')  # dif
graph_MACD.plot(np.arange(0, len(df_stockload.index)), macd_dea, 'blue', label='macd dea')  # dea

bar_red = np.where(macd_bar > 0, 2 * macd_bar, 0)# 绘制BAR>0 柱状图
bar_green = np.where(macd_bar < 0, 2 * macd_bar, 0)# 绘制BAR<0 柱状图
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_red, facecolor='red')
graph_MACD.bar(np.arange(0, len(df_stockload.index)), bar_green, facecolor='green')

graph_MACD.legend(loc='best',shadow=True, fontsize ='10')
graph_MACD.set_ylabel(u"MACD")
graph_MACD.set_xlim(0,len(df_stockload.index)) #设置一下x轴的范围
graph_MACD.set_xticks(range(0,len(df_stockload.index),15))#X轴刻度设定

#绘制KDJ
df_stockload['K'], df_stockload['D'] = talib.STOCH(df_stockload.high.values, df_stockload.low.values, df_stockload.close.values, \
                                                   fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

df_stockload['J'] = 3 * df_stockload['K'] - 2 * df_stockload['D']

graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['K'], 'blue', label='K')  # K
graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['D'], 'g--', label='D')  # D
graph_KDJ.plot(np.arange(0, len(df_stockload.index)), df_stockload['J'], 'r-', label='J')  # J
graph_KDJ.legend(loc='best', shadow=True, fontsize='10')

graph_KDJ.set_ylabel(u"KDJ")
graph_KDJ.set_xlabel("日期")
graph_KDJ.set_xlim(0, len(df_stockload.index))  # 设置一下x轴的范围
graph_KDJ.set_xticks(range(0, len(df_stockload.index), 15))  # X轴刻度设定 每15天标一个日期
graph_KDJ.set_xticklabels(
    [df_stockload.index.strftime('%Y-%m-%d')[index] for index in graph_KDJ.get_xticks()])  # 标签设置为日期

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
plt.savefig('Kline.jpg')
