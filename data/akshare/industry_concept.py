import datetime
import random
import time
import traceback

from retrying import retry
import akshare as ak
import pandas as pd

import configger
import utils.timeUtil
from logger.my_logger import logit
from utils.pdUtil import get_code_by_number, number_to_code
from utils.util import data_need_update


def delete_no_data(data,column):
    data=data.loc[data[column]!='暂无成份股数据']
    return data

def query_concept_names():
    data=ak.stock_board_concept_name_ths()
    data['update_time'] = datetime.datetime.now()
    return data
@number_to_code(column='代码')
def query_concept_infos(symbol):
    data = ak.stock_board_concept_cons_ths(symbol=symbol)
    data['update_time'] = datetime.datetime.now()
    data['概念'] = symbol
    data = delete_no_data(data, '代码')
    return data
def query_concept_index(symbol):
    data = ak.stock_board_concept_index_ths(symbol=symbol)
    data['update_time'] = datetime.datetime.now()
    data['概念'] = symbol
    data = delete_no_data(data, '日期')
    return data
def query_industry_names():
    data=ak.stock_board_industry_name_ths()
    data['update_time']=datetime.datetime.now()
    return data
@number_to_code(column='代码')
def query_industry_infos(symbol='半导体及元件'):
    data = ak.stock_board_industry_cons_ths(symbol=symbol)
    data['update_time'] = datetime.datetime.now()
    data['行业']=symbol
    data = delete_no_data(data, '代码')
    return data
def query_indsutry_index(symbol='半导体及元件'):
    data = ak.stock_board_industry_index_ths(symbol=symbol)
    data['update_time'] = datetime.datetime.now()
    data['行业'] = symbol
    data = delete_no_data(data, '日期')
    return data

@retry(wait_exponential_multiplier=5000, wait_exponential_max=5000,wrap_exception=False,stop_max_attempt_number=10)
def retry(fun,name):
    print(name,'start')
    time.sleep(3)
    data=fun(name)
    return data
# @retry(stop_max_attempt_number=7)
@logit()
def save_industry_data(seconds=100,way='byboot'):
    configger.init()
    engine = configger.engine
    wait_days=configger.constant_variables['low_ferquency_update_days']

    maintable = 'tb_ak_industry_names'
    indextable = 'tb_ak_industry_index'
    infotable = 'tb_ak_industry_infos'
    if(not utils.timeUtil.tableNeedUpdate(maintable)):
        return
    names = query_industry_names()
    names.to_sql(maintable, con=engine, if_exists='replace', index=False)
    print(names)
    if(utils.timeUtil.tableNeedUpdate(infotable,wait_days) or way=='byhand'):
        for name in names['name']:
            if(data_need_update(infotable,'update_time','行业',name)==False):
                continue
            data = retry(query_industry_infos,name)
            data.to_sql(infotable, con=engine, if_exists='append', index=False)
            print(data)
        utils.timeUtil.saveOperationTime(infotable)
    if(utils.timeUtil.tableNeedUpdate(indextable,wait_days) or way=='byhand'):
        for name in names['name']:
            if (data_need_update(indextable, 'update_time', '行业', name) == False):
                continue
            data = retry(query_indsutry_index,name)
            try:
                sql='select * from {} where 行业="{}"'.format(infotable,name)
                saved_data=pd.read_sql(sql=sql,con=engine)
                data=data.loc[not data['日期'].isin(saved_data['日期'])]
            except:
                traceback.print_exc()
            data.to_sql(indextable, con=engine, if_exists='append', index=False)
            print(data)
        utils.timeUtil.saveOperationTime(indextable)
    utils.timeUtil.saveOperationTime('tb_ak_industry_names')
@logit()
def save_concept_data(seconds=100,way='byboot'):
    configger.init()
    engine = configger.engine
    wait_days=configger.constant_variables['low_ferquency_update_days']
    if(not utils.timeUtil.tableNeedUpdate('tb_akshare_concept_names',wait_days)    ):
        return
    maintable = 'tb_ak_concept_names'
    indextable = 'tb_ak_concept_index'
    infotable = 'tb_ak_concept_infos'
    names = query_concept_names()
    names.to_sql(maintable, con=engine, if_exists='replace', index=False)
    print(names)
    if(not utils.timeUtil.tableNeedUpdate(infotable) or way=='byhand'):
        for name in names['name']:
            print(name)
            if (data_need_update(infotable, 'update_time', '概念', name) == False):
                continue
            data = retry(query_concept_infos, name)
            # data = query_concept_infos(name)
            data.to_sql(infotable, con=engine, if_exists='append', index=False)
            print(data)

        utils.timeUtil.saveOperationTime(infotable)

    if(not utils.timeUtil.tableNeedUpdate(indextable,wait_days)or way=='byhand'    ):
        for name in names['name']:
            if (data_need_update(indextable, 'update_time', '概念', name) == False):
                continue
            data = retry(query_concept_index, name)
            try:
                sql = 'select * from {} where 概念="{}"'.format(infotable, name)
                saved_data = pd.read_sql(sql=sql, con=engine)
                data = data.loc[not data['日期'].isin(saved_data['日期'])]
            except:
                traceback.print_exc()

            data.to_sql(indextable, con=engine, if_exists='append', index=False)
            print(data)
        utils.timeUtil.saveOperationTime(indextable)
    utils.timeUtil.saveOperationTime('tb_ak_concpet_names')

def save_data(seconds=100,way='byboot'):
    save_concept_data(seconds,way)
    save_industry_data(seconds,way)


if __name__=='__main__':
    save_data()