import pandas as pd

import configger
from mathUtils.average import findWeightAverage
from mathUtils.general import is_all_above_zero
from utils.pdUtil import getRecnetN


def select_growth_data(code='',n=12):
    configger.init()
    engine=configger.engine
    sql=configger.all_growthSQL
    if(code==''):
        data=pd.read_sql(sql=sql,con=engine)
    return data
def select_growth_data(code='',n=12):
    configger.init()
    engine = configger.engine
    sql = configger.all_growthSQL
    if (code == ''):
        data = pd.read_sql(sql=sql, con=engine)
    recent_data = data.groupby('code').apply(lambda x: getRecnetN(x, n))
    recent_data.index.names = ['code', 'index']
    recent_data.reset_index(inplace=True)
    recent_data.drop(columns='index', inplace=True)
    print(recent_data)
    return recent_data

def get_weight_average(data,sort_column='date',value_column='净利润-季度环比增长',n=12,is_above_zero=True):
    is_all=data.groupby('code').apply(lambda x: x[value_column].count() == n)
    is_all=is_all[is_all==True]
    tmp=data.loc[data['code'].isin(is_all.index)]
    last_date=tmp.groupby('code').apply(lambda x:x[sort_column].min()).max()
    res = data.groupby('code').apply(lambda x: findWeightAverage(x, sort_column=sort_column,value_column=value_column,n=n,last_date=last_date))
    if(is_above_zero==True):
        # print(data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column)))
        res.index.names=['code','index']
        res.reset_index(inplace=True)
        res.set_index('code',inplace=True)
        res.drop('index',inplace=True,axis=1)
        res['is_above_zero']=data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column))
        tmp=data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column))
        print(res['is_above_zero'])
        res=res.loc[res['is_above_zero']]
    print(res)
    return res