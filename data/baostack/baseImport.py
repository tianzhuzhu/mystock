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

import configger
from logger.my_logger import logit
from utils import util, timeUtil
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
    list=[]
    data=query_operation_data(code,year,quater)
    while (data.error_code == '0') & data.next():
        list.append(data.get_row_data())
    data = pd.DataFrame(list, columns=data.fields)
    return  data

def queryBalanceByCode(code,year,quater):
    list=[]
    data=query_balance_data(code,year,quater)
    while (data.error_code == '0') & data.next():
        list.append(data.get_row_data())
    data = pd.DataFrame(list, columns=data.fields)
    return data

def queryCashFlowByCode(code,year,quater):
    list=[]
    data=query_cash_flow_data(code,year,quater)
    while (data.error_code == '0') & data.next():
        list.append(data.get_row_data())
    data = pd.DataFrame(list, columns=data.fields)
    return data




def querHS300Stocks(date=''):
    rs = bs.query_hs300_stocks(date=date)
    # 打印结果集
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        hs300_stocks.append(rs.get_row_data())
    result = pd.DataFrame(hs300_stocks, columns=rs.fields)
def querySZ50Stocks(date=''):
    rs = bs.query_sz50_stocks(date)
    # 打印结果集
    sz50_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        sz50_stocks.append(rs.get_row_data())
    result = pd.DataFrame(sz50_stocks, columns=rs.fields)
def queryZZ500Stocks(date):
    rs = bs.query_zz500_stocks(date=date)
    # 打印结果集
    zz500_stocks = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        zz500_stocks.append(rs.get_row_data())
    result = pd.DataFrame(zz500_stocks, columns=rs.fields)
    return result
def queryStockIndustry(code,date=''):
    rs = bs.query_stock_industry(code=code,date=date)
    # 打印结果集
    industry_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        industry_list.append(rs.get_row_data())
    result = pd.DataFrame(industry_list, columns=rs.fields)
    return result
# query_history_k_data_plus

    # 结果集输出到csv文件

@logit()
def dataimport(table,fun,if_exists='append'):
    configger.init()
    engine=configger.engine
    stockData=todayStock()
    i,count =0, len(stockData.index)
    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)
    now=datetime.datetime.now()
    codes = tqdm(stockData['symbol'])
    sql='select code,max(updateTime) as updateTime,max(date) as date from {}  GROUP BY code '.format(table)
    try:
        timeData=pd.read_sql(con=engine,sql=sql,index_col='code')
    except:
        timeData=pd.DataFrame()
    # print(timeData)
    for code in codes:
        data=pd.DataFrame()
        try:
            if(not timeData.empty and code in timeData.index and (now-timeData.loc[code,'updateTime']).days<1):
                # print(timeData.loc[code])
                continue
        except:
            traceback.print_exc()
            pass
        # sql='select max(date) from {} where  code="{}"'.format(table,code)
        i=i+1
        try:
            # print('timeData',timeData)
            date=timeData.loc[code,'date']
            # print('date',date)
            year,season=date.split('-')
            year,season=int(year),int(season)
        except:
            year=1989
            season=4

        season=season+1
        year =year+1 if(season==5) else year
        season =0 if(season==5) else season
        # print('update',year,season)
        # print(year,season)
        list=[]
        for i in range(year,toyear+1):
            for j in range(1,5):
                #在之前
                if(i==year and j<season) or i < year:
                    continue
                #在以后
                elif(i==toyear and j>toseason) or i>toyear:
                    continue
                #更新
                else:
                    list.append(i*10+j)
        list.reverse()
        j = 0
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            try:
                # print(i)
                result=fun(code,int(i/10),i%10)
                result['code']=code
                result['date']=date
                ##判断无历史数据自动跳出
                if(result.empty):
                    j=j+1
                    if(j>3):
                        break
                    continue
                if(data is None or data.empty):
                    data=result
                else:
                    data=data.append(result,ignore_index=True)
                    # print(count)
                # print(data)
            except:
                traceback.print_exc()
        data['updateTime']=now
        # print(data)
        data.to_sql(table,con=engine,if_exists=if_exists,index=False)
        # print(data)
        os.system('cls')
        if(i%100==0):
            bs.logout()
            time.sleep(5)
            bs.login()
        codes.set_description("导入{}中代码为{},条数为{}".format(table,code,len(data.index)))
    bs.logout()
def importBasicData(table,fun,if_exists='append'):
    if(timeUtil.tableNeedUpdate(table)):
        dataimport(table,fun,if_exists='append')
    timeUtil.saveOperationTime(table)

def mainProcess():
    configger.init()
    engine=configger.engine
    stockData=todayStock()
    # importData(stockData,engine,table,queryGrowthByCode)
if __name__ == '__main__':
    mainProcess()