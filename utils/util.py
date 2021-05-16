import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
import talib
from sqlalchemy import create_engine, VARCHAR
import numpy as np
import database


class util():
    def __init__(self):
        self.engine=create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    def __init__(self,engine=create_engine('mysql+pymysql://root:root@localhost:3306/stock')
                 ):
        self.engine=engine
    def getKBySymbol(self,symobl,days=None):
        engine=self.engine
        if(days==None):
            sql='select * from tb_stock_hisotry_detatil where code="{}"  order by date desc'.format(symobl)
        else:
            sql='select * from tb_stock_hisotry_detatil where code="{}"  order by date desc limit 0,{}'.format(symobl,days)
        # print(sql)
        data=pd.read_sql(sql,con=engine)
        data.set_index('date',inplace=True)
        data.sort_index(ascending=True,inplace=True)
        return data
    def saveData(data,engine,table):
        try:
            data.to_sql(table,con=engine)
        except:
            traceback.print_exc()
    def getdotCodeBysymbol(code):
        code=list(code)
        code.insert(2,'.')
        code=''.join(code)
        return code
    def getsql(sql_path):
        sql = open(sql_path, "r", encoding="utf8")
        sql = sql.readlines()
        sql = "".join(sql)
        return sql
def needUpdate(lastUpdateTime,nowtime,isWorkDay=False):
    # 2021-04-01 08:00:00	2021-04-02 00:00:00
    #工作日判断尚未完成
    if(nowtime.hour<15):
        nowtime= nowtime - datetime.timedelta(days=1)
    if(lastUpdateTime.hour<15):
        lastUpdateTime= lastUpdateTime - datetime.timedelta(days=1)
    days=(nowtime.date()-lastUpdateTime.date()).days
    if(isWorkDay==True):
        #3天必更
        if(days>=3):
            return True
        if(days==2):
            if(nowtime.weekday()==6):
                return False
            else: return True
        if(days==1):
            if(nowtime.weekday()==6 or nowtime.weekday()==5):
                return False
            else: return True
        return False

    else:
        #非工作日判断
        #隔了2天
        if(days>=1):
            return True
        else:
            return False
def todayStock(table='tb_today_stock'):

    nowtime = datetime.datetime.now()

    endDate = nowtime.strftime('%Y%m%d')
    createTimeSql=" SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = '{}' and `information_schema`.`TABLES`.`TABLE_NAME` = '{}' ".format('stock',table)

    database.init()
    engine=database.engine
    lastUpdateTime=pd.read_sql(con=engine,sql=createTimeSql).iloc[0,0]
    try:
        ##排除五点后获取数据
        print('needUpdate')
        print(needUpdate(lastUpdateTime,nowtime,isWorkDay=True))
        if(needUpdate(lastUpdateTime,nowtime)):
            stockData = ak.stock_zh_a_spot()
            stockData['symbol']=stockData['symbol'].map(lambda x:getdotCodeBysymbol(x))
            stockData.to_sql(table,con=engine,if_exists='replace')
        else:
            stockData=pd.read_sql(con=engine,sql='select * from {}'.format(table))
    except:
        # traceback.print_exc()
        stockData = ak.stock_zh_a_spot()
        stockData['symbol']=stockData['symbol'].map(lambda x:getdotCodeBysymbol(x))
        stockData.to_sql(table,con=engine,if_exists='replace')

    return stockData
def saveData(data,engine,table):
    try:
        data.to_sql(table,con=engine)
    except:
        traceback.print_exc()
def getdotCodeBysymbol(code):
    code=list(code)
    code.insert(2,'.')
    code=''.join(code)
    return code
def removedotBysymbol(code):
    try:
        i=code.find('.')
        code=code[0:i]+code[i+1:]
    except:
        pass
    return code
def getsql(sql_path):
    sql = open(sql_path, "r", encoding="utf8")
    sql = sql.readlines()
    sql = "".join(sql)
    return sql
def getKBySymbol(symobl,days=None):
    database.init()
    engine=database.engine
    if(days==None):
        sql='select * from tb_stock_hisotry_detatil where code="{}"  order by date desc'.format(symobl)
    else:
        sql='select * from tb_stock_hisotry_detatil where code="{}"  order by date desc limit 0,{}'.format(symobl,days)
    # print(sql)
    data=pd.read_sql(sql,con=engine)
    data.set_index('date',inplace=True)
    data.sort_index(ascending=True,inplace=True)
    return data
def getMacdByData(data,fast=12,slow=26,signal=9):
    try:
        data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['close'],fastperiod=fast, slowperiod=slow, signalperiod=signal)

    except:
        data["macd"], data["macd_signal"], data["macd_hist"] = talib.MACD(data['Close'],fastperiod=fast, slowperiod=slow, signalperiod=signal)

    return data
def getMaBydata(data,MAlist):
    if('Close' in data.index.tolist()):
        close='Close'
    elif('close' in data.columns.tolist()):
        close='close'
    else:
        return
    for i in MAlist:
        data["ma"+str(i)] = talib.MA(data[close], timeperiod=i)
    # print(data)
    return data
def getMarketValueBySymbol(symbol):
    database.init()
    engine=database.engine
    sql1="select totalShare from tb_profit WHERE code='{}' ORDER BY date desc limit 0,1".format(symbol)
    sql1.format(symbol)
    sql2="select close from tb_stock_hisotry_detatil WHERE code='{}' ORDER BY date desc limit 0,1".format(symbol)
    sql2.format(symbol)

    totalShare=np.float64(pd.read_sql(con=engine,sql=sql1).iloc[0,0])
    price=np.float64(pd.read_sql(con=engine,sql=sql2).iloc[0,0])
    # print(totalShare)
    # print(price)
    marketValue=totalShare*price
    return  marketValue
def getAllMarketValue():
    database.init()
    engine=database.engine
    sqlCloseValue='select t.* from (' \
                  'SELECT max(date) as date,code  FROM tb_stock_hisotry_detatil  GROUP BY code) o ,  tb_stock_hisotry_detatil t where t.code=o.code and t.date=o.date'
    sqlShare='select t.* from ' \
             '(SELECT max(date) as date,code  FROM tb_profit  GROUP BY code) o ,  tb_profit t where t.code=o.code and t.date=o.date'
    priceData=pd.read_sql(con=engine,sql=sqlCloseValue,index_col='code')
    ShareData=pd.read_sql(con=engine,sql=sqlShare,index_col='code')
    marketData=pd.DataFrame(index=priceData.index)
    nowdate=datetime.datetime.now().date()
    marketData['totalMarketValue']=priceData['close']*ShareData['totalShare']
    marketData['liquidMarketValue']=priceData['close']*ShareData['liqaShare']
    marketData['roeAvg']=ShareData['roeAvg']
    marketData['npMargin']=ShareData['npMargin']
    marketData['netProfit']=ShareData['netProfit']
    marketData['epsTTM']=ShareData['epsTTM']
    marketData['MBRevenue']=ShareData['MBRevenue']
    marketData['totalShare']=ShareData['totalShare']
    marketData['liqaShare']=ShareData['liqaShare']
    marketData['updateTime']=nowdate
    marketData.to_sql(con=engine,name='tb_basic_information',if_exists='replace',dtype={'code':VARCHAR(32)})

    return marketData
def findDataBymarkevalueTH(totalMarketValuelowTh,totalMarketValueHighTh=0,liquidMarketValueLowTh=0,liquidMarketValueHighTh=0):
    database.init()
    engine=database.engine
    sqlBasicInformation='select * from tb_basic_information'
    basicinformation=pd.read_sql(sql=sqlBasicInformation,con=engine,index_col='code')
    # print(basicinformation)
    totalMarketValuelowTh,totalMarketValueHighTh,liquidMarketValueHighTh,liquidMarketValueLowTh=totalMarketValuelowTh*100000000,totalMarketValueHighTh*100000000,liquidMarketValueHighTh*100000000,liquidMarketValueLowTh*100000000
    basicinformation=basicinformation.loc[ \
        basicinformation['totalMarketValue']>totalMarketValuelowTh]
    if(totalMarketValueHighTh!=0):
        basicinformation=basicinformation.loc[ \
            basicinformation['totalMarketValue']<totalMarketValueHighTh]
        # basicinformation['liquidMarketVAlue']>liquidMarketValueTh]
    # path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\{}'.format(date)
    # if(not os.path.exists(path)):
    #     os.mkdir(path)
    # filepath=os.path.join(path,'结果{}-{}.xlsx'.format(str(k),str(growth)))

    # myEmail.send.send_mail(filepath)
    return basicinformation
def getRecentDataBydata(data):

    database.init()
    engine=database.engine
    if(data.index.name!='code'):
        data.set_index('code',inplace=True)
    list=data.index.tolist()
    for i in range(len(list)):
        list[i]="'"+list[i]+"'"

    codes=','.join(list)
    sql="select t.* from (" \
        "SELECT max(date) as date,code  FROM tb_stock_hisotry_detatil  e where code in " \
        "({}) GROUP BY code)o ,  tb_stock_hisotry_detatil t where t.code=o.code and t.date=o.date".format(codes)
    result=pd.read_sql(sql=sql,con=engine,index_col='code')
    result=pd.concat([data,result],axis=1)
    # print(result)
    return result

def findGrowhBydata(data,grow=.3):
    database.init()
    engine=database.engine
    if(data.index.name!='code'):
        data.set_index('code',inplace=True)
    list=data.index.tolist()
    for i in range(len(list)):
        list[i]="'"+list[i]+"'"
    codes=','.join(list)
    sql='select t.* from tb_growth t,' \
        '(select max(date) as date,code from tb_growth where code in ({}) GROUP BY code) o ' \
        'where t.code=o.code and t.date=o.date'.format(codes)

    result=pd.read_sql(sql=sql,con=engine,index_col='code')
    # print(result['YOYNI'])

    result=pd.concat([data,result],axis=1)
    result['YOYNI']=  result['YOYNI'].apply(float)
    result=result.loc[result['YOYNI']>grow]
    # print(result['YOYNI'])
    # print(result)
    result.index.name='code'
    return result


def fliterPeByData(data,peTh=30):
    if('peTTM' in data.columns):
        data=data.loc[data['peTTM']<=peTh]
        data['peTTM']=  data['peTTM'].apply(float)
        data=data.loc[data['peTTM']>0]
    else:
        data=getRecentDataBydata(data)
        data['peTTM']=  data['peTTM'].apply(float)
        data=data.loc[data['peTTM']<=0]
    return data
def findVolume(x,n):
    x=x[0:n]

    x['date']=pd.to_datetime(x['date'])
    maxDate=x['date'].max()
    todayvolume=x.loc[maxDate==x['date'],'volume'].iloc[0]
    x['close']=  x['close'].apply(float)
    avg=x['close'].mean()

    sumv=(x['volume']>todayvolume).apply(int).sum()
    # return pd.Series({'sum':sumv,'增长率':data.iloc[0,0],'pe':data.iloc[0,1],'pb':data.iloc[0,2]})

    return sumv
def findVolumeCountByData(data,days=100):
    database.init()
    engine=database.engine
    list=data.index.tolist()
    for i in range(len(list)):
        list[i]="'"+list[i]+"'"
    codes=','.join(list)
    sql="select * from tb_stock_hisotry_detatil WHERE code in ({})".format(codes)
    volumes=pd.read_sql(sql=sql,con=engine,index_col='code')
    data['count']=volumes.groupby(['code']).apply(lambda x:findVolume(x,days))
    data.sort_values(by=['YOYNI','count'])
    return data