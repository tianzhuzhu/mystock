import datetime
import random
import time
import traceback

from retrying import retry
import akshare as ak
import pandas as pd

import database
import utils.timeUtil
from utils.util import data_need_update


def delete_no_data(data,column):
    data=data.loc[data[column]!='暂无成份股数据']
    return data
def query_concept_names():
    data=ak.stock_board_concept_name_ths()
    data['update_time'] = datetime.datetime.now()
    return data
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

@retry(wait_exponential_multiplier=5000, wait_exponential_max=50000,wrap_exception=False)
def retry(fun,name):
    time.sleep(random.randint(10))
    data=fun(name)
    return data
# @retry(stop_max_attempt_number=7)
def save_data(seconds=100):
    database.init()
    engine = database.engine
    utils.timeUtil.tableNeedUpdate('tb_akshare_industry_names')
    maintable = 'tb_ak_industry_names'
    indextable = 'tb_ak_industry_index'
    infotable = 'tb_ak_industry_infos'

    names = query_industry_names()
    names.to_sql(maintable, con=engine, if_exists='replace', index=False)
    print(names)
    for name in names['name']:
        if(data_need_update(infotable,'update_time','行业',name)==False):
            continue
        data = retry(query_industry_infos,name)
        data.to_sql(infotable, con=engine, if_exists='append', index=False)
        print(data)
    for name in names['name']:
        if (data_need_update(indextable, 'update_time', '行业', name) == False):
            continue

        data = retry(query_indsutry_index,name)
        try:
            sql='select * from {} where 行业="{}"'.format(infotable,name)
            saved_data=pd.read_sql(sql=sql,con=engine)
            data=data.loc[~data['日期'].isin(saved_data['日期'])]
        except:
            traceback.print_exc()


        data.to_sql(indextable, con=engine, if_exists='append', index=False)
        print(data)
    utils.timeUtil.saveOperationTime('tb_ak_industry_names')

    utils.timeUtil.tableNeedUpdate('tb_akshare_concept_names')
    maintable = 'tb_ak_concept_names'
    indextable = 'tb_ak_concept_index'
    infotable = 'tb_ak_concept_infos'

    names = query_concept_names()
    names.to_sql(maintable, con=engine, if_exists='replace', index=False)
    print(names)
    for name in names['name']:
        print(name)
        if (data_need_update(infotable, 'update_time', '概念', name) == False):
            continue
        data = retry(query_concept_infos, name)
        data.to_sql(infotable, con=engine, if_exists='replace', index=False)
        print(data)
    for name in names['name']:
        if (data_need_update(indextable, 'update_time', '概念', name) == False):
            continue
        data = retry(query_concept_index, name)
        try:
            sql = 'select * from {} where 概念="{}"'.format(infotable, name)
            saved_data = pd.read_sql(sql=sql, con=engine)
            data = data.loc[~data['日期'].isin(saved_data['日期'])]
        except:
            traceback.print_exc()

        data.to_sql(indextable, con=engine, if_exists='append', index=False)
        print(data)
    utils.timeUtil.saveOperationTime('tb_ak_concpet_names')


if __name__=='__main__':
    save_data()