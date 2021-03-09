import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import pymysql
# stock_df = ak.stock_zh_index_spot()
# print(stock_df)

def importTodayStock():
    stockData = ak.stock_zh_a_spot()
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    stockData.to_sql('todaystock',con=engine,if_exists='replace')
def GetStockHistory(symbol,startdate,enddate):
    data = ak.stock_zh_a_daily(symbol=symbol, start_date=startdate, end_date=enddate, adjust="qfq")
    # stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20101103", end_date="20201116", adjust="qfq")
    data['symbol']=symbol
    return data
def getPe(code,date='19900101'):
    # engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    # sql=('select max(trade_date) from pehistory where code ="{}"'.format(code))
    BasicData = ak.stock_a_lg_indicator(stock=code)
    BasicData=BasicData.loc[BasicData['trade_date']>date]
    return BasicData
    # print('BasicData')
    # BasicData.to_sql('pehistory', con=engine, if_exists='append')
def insertTotalData(code,startDate,endate,engine):
    if(pd.to_datetime(startDate)>pd.to_datetime(endate)):
        return
    pelist=[]
    print(startDate,endate)
    print('获取代码',code,'数据')
    try:
        data=GetStockHistory(code,startDate,endate)
        # data['code']=code 52126772
    except:
        try:
            data=GetStockHistory(code,startDate,endate)
        except:
            time.sleep(random.randint(1,10))
            print('get',code,'except')
    try:
        if(data is None or not data.empty):
            print(data)
            data.to_sql('stockhistory',con=engine,if_exists='append')

    except Exception as ex:

        print('sql exception')
        traceback.print_exc()
    print(code,'finshed')
    time.sleep(random.randint(1,2)*0.1)

def insertTodayValue(endDate):
    createTimeSql=" SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "

    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    createTime=pd.read_sql(con=engine,sql=createTimeSql)
    if(datetime.datetime.now().day!=createTime.iloc[0,0].day):
        stockData = ak.stock_zh_a_spot()
        stockData.to_sql('todaystock',con=engine,if_exists='replace')
    else:
        stockData=pd.read_sql(con=engine,sql='select * from todaystock')

    i=0
    for code in stockData['symbol']:
        try:
            lastDate=pd.read_sql(con=engine,sql='select max(date) from stockhistory where symbol="{}"'.format(code))
            lastDate=lastDate.iloc[0,0]
            # print('lastdate',lastDate)
            if(pd.to_datetime(lastDate).date()==datetime.datetime.now().date()):
                continue
                print('重复数据')

            lastDate=pd.to_datetime(pd.to_datetime(lastDate)+datetime.timedelta(days=1))
            print(lastDate)
        except:
            # traceback.print_exc()
            lastDate='19900101'
        # print('下一天日期',lastDate)
        i=i+1
        print('开始第',i,'条数据')
        insertTotalData(code,lastDate,endDate,engine)
        # lastDate.
        #

if __name__ == '__main__':
    today = datetime.datetime.now()
    endDate = today.strftime('%Y%m%d')
    insertTodayValue(endDate)