import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
from sqlalchemy import create_engine

def todayStockData():
    today = datetime.datetime.now()
    endDate = today.strftime('%Y%m%d')
    createTimeSql=" SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "

    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    createTime=pd.read_sql(con=engine,sql=createTimeSql)
    if(datetime.datetime.now().day!=createTime.iloc[0,0].day):
        stockData = ak.stock_zh_a_spot()
        stockData.to_sql('todaystock',con=engine,if_exists='replace')
    else:
        stockData=pd.read_sql(con=engine,sql='select * from todayStock')

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