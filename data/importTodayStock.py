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
from tqdm import tqdm

import database
from utils import util
from utils.util import removedotBysymbol, todayStock


def importTodayStock():
    stockData = ak.stock_zh_a_spot()
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    stockData.to_sql('todaystock',con=engine,if_exists='replace')
def GetStockHistory(symbol,startdate,enddate):
    symbol=removedotBysymbol(symbol)
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
    # print(startDate,endate)
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
        if(not data is None or not data.empty):
            # print(data)
            data.to_sql('stockhistory',con=engine,if_exists='append')

    except Exception as ex:

        print('sql exception')
        traceback.print_exc()
    print(code,'finshed')
    # time.sleep(random.randint(1,2)*0.01)

def insertTodayValue(data,table):
    today = datetime.datetime.now()
    database.init()
    engine=database.engine

    i=0
    symbols = tqdm(data['symbol'])
    now=datetime.datetime.now()
    sql='select code,max(date) as date,max(updateTime)as updateTime from {}  GROUP BY code'.format(table)
    # print(sql)
    try:
        timeData=pd.read_sql(con=engine,sql=sql,index_col='code')
    except:
        timeData=pd.DataFrame()
    # print(timeData)
    for code in symbols:
        code=util.removedotBysymbol(code)
        i=i+1
        # code=util.getdotCodeBysymbol(symbol)
        try:
            if(not timeData.empty and code in timeData.index and (now-timeData.loc[code,'updateTime']).seconds<3600*24):
                continue
        except:
            pass
        try:
            start_date= pd.to_datetime(timeData.loc[code,'date']) + datetime.timedelta(days=1)
            start_date=start_date.strftime('%Y%m%d')
            # start_date=start_date.date()
        except:
            start_date='19900101'
            # traceback.print_exc()
        end_date=today.strftime('%Y-%m-%d')
        # print(start_date,end_date)
        if(start_date>end_date):
            # print(code,start_date,'已存在')
            continue
        # print('star_Date')
        # print(start_date)

        result=ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date, adjust="qfq")
        result.reset_index(inplace=True)
        result['updateTime']=now
        result['code']=code
        print(result)

        result.to_sql(table,con=engine,if_exists='append',index=False)
        symbols.set_description("查询代码为：{},数据条数为{}".format(code,len(result.index)))

def importToday():
    today = datetime.datetime.now()
    endDate = today.strftime('%Y%m%d')
    data=util.todayStock()
    insertTodayValue(data,'tb_stock_history')
if __name__ == '__main__':
    importToday()