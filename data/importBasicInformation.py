import datetime
import os
import time
import traceback
import akshare as ak
import baostock as bs
import pandas as pd
from baostock import query_operation_data, query_balance_data, query_cash_flow_data, query_performance_express_report, \
    query_forecast_report
from tqdm import tqdm
# 登陆系统
from sqlalchemy import create_engine

import database
from utils import util
from utils.util import todayStock


def queryProfitByCode(code,year,season):
    # 查询季频估值指标盈利能力
    profit_list = []
    rs_profit = bs.query_profit_data(code=code, year=year, quarter=season)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    return result_profit

def queryDubpontByCode(code,year,quater):
    dupont_list = []
    rs_dupont = bs.query_dupont_data(code=code, year=year, quarter=quater)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    return result_profit

def queryGrowthByCode(code,year=None,quater=None):
    growth_list = []
    rs_growth = bs.query_growth_data(code=code, year=year, quarter=quater)
    while (rs_growth.error_code == '0') & rs_growth.next():
        growth_list.append(rs_growth.get_row_data())
    result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
    return  result_growth

def queryOperationByCode(code,year,quater):
    query_operation_data(code,year,quater)

def queryBalanceByCode(code,year,quater):
    query_balance_data(code,year,quater)

def queryCashFlowByCode(code,year,quater):
    query_cash_flow_data(code,year,quater)

def queryPerformanceExpressReportByCode(code,year,quater):
    query_performance_express_report(code,year,quater)
def queryForecastReport(code,year,quater):
    query_forecast_report(code,year,quater)

# query_hs300_stocks()
# query_sz50_stocks()
# query_zz500_stocks()
# query_stock_industry(code,date
# query_history_k_data_plus

    # 结果集输出到csv文件



def importBasicData(table,fun):
    database.init()
    engine=database.engine
    stockData=todayStock()
    i,count =0, len(stockData.index)
    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)+1
    codes = tqdm(stockData['symbol'])
    for code in codes:
        # print(code)
        data=pd.DataFrame()
        # print(code)
        # print(code)
        now=datetime.datetime.now()
        sql='select max(updateTime) from {} where  code="{}"'.format(table,code)
        try:

            updateTime=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            if(now-updateTime).seconds>7200:
                continue
        except:
            pass
        sql='select max(date) from {} where  code="{}"'.format(table,code)
        i=i+1
        try:
            date=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            year,season=date.split('-')
            year,season=int(year),int(season)
        except:
            year=1989
            season=4

        season=season+1
        year =year+1 if(season==5) else year
        season =0 if(season==5) else season
        # print(year,season)
        list=[]
        for i in range(year,toyear+1):
            for j in range(1,5):
                #最后一次数据的年
                if(i==year and j>=season):
                    list.append(i*10+j)
                #今年
                elif(i==toyear and j<=toseason):
                    list.append(i*10+j)
                #中间年
                elif(i>year and i<toyear):
                    list.append(i*10+j)
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            try:
                result=fun(code,int(i/10),i%10)
                result['code']=code
                result['date']=date

                if(data is None or data.empty):
                    data=result
                else:
                    data=data.append(result,ignore_index=True)
                    # print(count)
            except:
                traceback.print_exc()
        # time.sleep(0.5)
        # print(data)
        data['updateDate']=datetime.datetime.now()
        data.to_sql(table,con=engine,if_exists='append',index=False)
        # print(stockData)
        bar = stockData['symbol']
        # progress_bar = tqdm(bar)
        os.system('cls')
        if(i%200==0):
            bs.logout()
            time.sleep(5)
            bs.login()
        codes.set_description("导入{}中代码为{},条数为{}".format(table,code,len(data.index)))
        # with tqdm(total=count) as pbar:
        #     print(i)

        #     pbar.update(i)
        # i = i + 1
    bs.logout()
def mainProcess():
    database.init()
    engine=database.engine
    stockData=todayStock()
    # importData(stockData,engine,table,queryGrowthByCode)
if __name__ == '__main__':
    mainProcess()