import datetime
import random
import time
import traceback
import util

import akshare as ak
import pandas as pd
import baostock as bs
from sqlalchemy import create_engine

keys= {'利润表':'tb_income_statement','资产负债表':'tb_balance_sheet','现金流量表':'tb_flow_cash'}
def save_table(data,v,i):
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_detail')
    if(i>20):
        print('超过20张表')
        return
    try:
        data.to_sql(v +"_"+str(i), con=engine, if_exists='append',index=False)
        print('数据存储在',v+str(i)  ,'中')
    except:
        i=i+1
        save_table(data,v,i)
def importByCodeKV(code,k,v):
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock_detail')
    flag=0
    try:
        for i in range(20):
            try:
                sql = 'select count(1) from {} where code ="{}"'.format(v+"_"+str(i), code)
                data = pd.read_sql(con=engine, sql=sql)
                if(data.iloc[0,0]>0):
                    flag=1
            except:
                pass
        if(flag==1):
            print(code,k,'pass')
            return
        result = ak.stock_financial_report_sina(stock=code, symbol=k)

        # Balance sheet Cash flow statement Income statement
        time.sleep(random(1, 10)*0.1)
        result = ak.stock_financial_report_sina(stock=code, symbol=k)
        result = result.loc[result['报表日期'].isin[data['报表日期']]]
        result.rename(columns={'一、营业总收入':'一、营业收入'},inplace=True)
    except:
        result = ak.stock_financial_report_sina(stock=code, symbol=k)
    result['code'] = code
    print(result)
    save_table(result,v,0)
def importByCode(code,engine):
    for k,v in keys.items():
        print(code,k,v,'开始')
        try:

            importByCodeKV(code,engine,k,v)
            print(code, k, v, '顺利结束')
        except:
            try:
                time.sleep(10)
                importByCodeKV(code, k, v)
                print(code, k, v, '顺利结束')
            except:
                print(code,k,v,'失败')

def mainProcess():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    stockData= util.todayStockData()
    importByCode('600519',engine)
    for code in stockData['code']:
        importByCode(code,engine)
if __name__=='__main__':
    mainProcess()