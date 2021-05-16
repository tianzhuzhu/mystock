import datetime
import os
import time
import traceback
import akshare as ak
import baostock as bs
import pandas as pd
from baostock import query_operation_data, query_balance_data, query_cash_flow_data, query_performance_express_report, \
    query_forecast_report, query_hs300_stocks
from tqdm import tqdm
# 登陆系统
import logging
from sqlalchemy import create_engine
import database
from utils import util
from utils.util import todayStock, needUpdate


def queryPerformanceExpressReportByCode(code,starDate):
    list=[]
    data=query_performance_express_report(code,start_date=starDate)
    while (data.error_code == '0') & data.next():
        list.append(data.get_row_data())
    data = pd.DataFrame(list, columns=data.fields)
    return data
def queryForecastReport(code,starDate):
    list=[]
    data=query_forecast_report(code,start_date=starDate)
    while (data.error_code == '0') & data.next():
        list.append(data.get_row_data())
    data = pd.DataFrame(list, columns=data.fields)
    return data
def importReport(table,fun,if_exists='append'):
    today = datetime.datetime.now()
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler("log.txt")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(table+' start')
    database.init()
    engine=database.engine
    data=todayStock()
    lg = bs.login()
    i=0
    symbols = tqdm(data['symbol'])
    now=datetime.datetime.now()
    sql='select code,max(date) as date,max(updateTime)as updateTime from {}  GROUP BY code'.format(table)
    try:
        timeData=pd.read_sql(con=engine,sql=sql,index_col='code')
    except:
        timeData=pd.DataFrame()
    for code in symbols:
        i=i+1
        # code=util.getdotCodeBysymbol(symbol)
        if(not timeData.empty and code in timeData.index and needUpdate(timeData.loc[code,'updateTime'],now,isWorkDay=True)==False):
            continue
        try:
            start_date= pd.to_datetime(timeData.loc[code,'date']) + datetime.timedelta(days=90)
            start_date=start_date.strftime('%Y-%m-%d')
            # start_date=start_date.date()
        except:
            start_date='1990-01-01'
        # print(start_date,end_date)
        # print(start_date,end_date)
        result=fun(code,start_date)
        result['updateTime']=now
        # print(result)
        result.to_sql(table,con=engine,if_exists=if_exists,index=False)
        symbols.set_description("查询代码为：{},数据条数为{}".format(code,len(result.index)))
        if(i%1000==0):
            bs.logout()
            time.sleep(5)
            bs.login()
    bs.logout()