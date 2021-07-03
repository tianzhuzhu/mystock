import datetime
import logging
import traceback

import akshare as ak
import pandas as pd
import retrying

import configger
from logger.my_logger import logit
from utils import pdUtil, timeUtil
from utils.pdUtil import number_to_code



def get_last_yjbb_by_date(date=''):
    if(date==''):
        date=datetime.datetime.now()
    date=timeUtil.get_last_end_quarter_day(date).date()
    query_time=str(date.strftime("%Y%m%d"))
    print(query_time)
    try:
        data = ak.stock_em_yjbb(date=query_time)
        data['date']=date
        data.rename(columns={'股票代码':'code'},inplace=True)
    except:
        traceback.print_exc()
        return None
    try:
        data.drop(columns=['序号'],inplace=True)
    except:
        pass
    return data
@number_to_code(column='code')
@retrying.retry()
def get_yjbb_by_date(date='',fun=ak.stock_em_yjbb):
    query_time=str(date.strftime("%Y%m%d"))
    try:
        data = fun(date=query_time)
        data['date']=date
        data.rename(columns={'股票代码':'code'},inplace=True)
        data=pdUtil.get_code_by_number(data,'code')
    except:
        return None
    try:
        data.drop(columns=['序号'],inplace=True)
    except:
        pass
    return data
#stock_em_yjkb
#stock_em_yjyg
#stock_em_yysj
#stock_em_zcfz
#stock_em_lrb
#stock_em_xjll

def select_yjbb_by_date(tablename,date):
    sql='select * from {} where date ={}'.format(tablename,date)
    try:
        configger.init()
        engine=configger.engine
        result=pd.read_sql(sql=sql,con=engine)
        return result
    except:
        print('select_yjbb_by_date error {}'.format(date))
@logit()

def update_yjbb_to_db(tablename='',fun=ak.stock_em_yjbb,way='byboot'):
    configger.init()
    engine = configger.engine
    now=datetime.datetime.now()
    if(timeUtil.tableNeedUpdate(tablename)==False and way=='byboot'):
        return False
    try:
        sql='select max(date) from {}'.format(tablename)
        last_update_date=pd.read_sql(sql=sql,con=engine).iloc[0,0]
        last_update_date = timeUtil.get_this_end_quarter_day(last_update_date)
    except:
        last_update_date=pd.to_datetime('1991-1-1')
        last_update_date = timeUtil.get_this_end_quarter_day(last_update_date)
    print(last_update_date,last_update_date)
    this_end_season=timeUtil.get_this_end_quarter_day(now)

    #处理部分未更新数据
    #处理全量数据
    season_end=pd.period_range(start=last_update_date,end=this_end_season,freq='q')
    season_end=pd.to_datetime(season_end.values.astype('datetime64[D]'))
    print(season_end)
    resultlist=[]
    for date in season_end:
        data=get_yjbb_by_date(date,fun)
        print(data)
        if(data is None):
            print(tablename+' '+str(date)+' have no data')
            continue
        data['update_time']=now
        try:
            sql = 'select * from {} where date="{}"'.format(tablename, date.date())
            print(sql)
            saved_data=pd.read_sql(sql=sql,con=engine)
            print(data['code'].isin(saved_data['code']))
            data=data=data.loc[~data['code'].isin(saved_data['code'])]
            resultlist.append(data)
        except:
            resultlist.append(data)
    for data in resultlist:
        if(not data.empty):
            print(data)
            data.to_sql(tablename,con=engine,if_exists='append',index=False)
    timeUtil.saveOperationTime(tablename)
def update_allow_basic_information(way='byboot'):
    dict = {
        'tb_ak_bi_yjbb': ak.stock_em_yjbb,
        'tb_ak_bi_quick_report': ak.stock_em_yjkb,
        'tb_ak_bi_forecast_report': ak.stock_em_yjyg,
        'tb_ak_bi_disclosure_time': ak.stock_em_yysj,
        'tb_ak_bi_balance_sheet': ak.stock_em_zcfz,
        'tb_ak_bi_interst': ak.stock_em_lrb,
        'tb_ak_bi_cash_flow': ak.stock_em_xjll,
    }
    for k,v in dict.items():
        update_yjbb_to_db(tablename=k,fun=v,way=way)
if __name__=='__main__':
    update_yjbb_to_db('tb_bi_akshare_yjbb')




