import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
import talib
from sqlalchemy import create_engine

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
    def todayStockData(self):
        engine=self.engine
        today = datetime.datetime.now()
        endDate = today.strftime('%Y%m%d')
        createTimeSql=" SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "
        createTime=pd.read_sql(con=engine,sql=createTimeSql)
        try:
            if(datetime.datetime.now().day!=createTime.iloc[0,0].day):
                stockData = ak.stock_zh_a_spot()
                stockData.to_sql('todaystock',con=engine,if_exists='replace')
            else:
                stockData=pd.read_sql(con=engine,sql='select * from todayStock')
        except:
            stockData = ak.stock_zh_a_spot()
            stockData.to_sql('todaystock',con=engine,if_exists='replace')
        stockData['symbol']=stockData['symbol'].map(lambda x:getdotCodeBysymbol(x))
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
    def getsql(sql_path):
        sql = open(sql_path, "r", encoding="utf8")
        sql = sql.readlines()
        sql = "".join(sql)
        return sql

# @static_vars(engine=0)
def todayStockData():
    today = datetime.datetime.now()
    endDate = today.strftime('%Y%m%d')
    createTimeSql=" SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "

    database.init()
    engine=database.engine
    createTime=pd.read_sql(con=engine,sql=createTimeSql)
    try:
        if(datetime.datetime.now().day!=createTime.iloc[0,0].day):
            stockData = ak.stock_zh_a_spot()
            stockData.to_sql('todaystock',con=engine,if_exists='replace')
        else:
            stockData=pd.read_sql(con=engine,sql='select * from todayStock')
    except:
        stockData = ak.stock_zh_a_spot()
        stockData.to_sql('todaystock',con=engine,if_exists='replace')
    stockData['symbol']=stockData['symbol'].map(lambda x:getdotCodeBysymbol(x))
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