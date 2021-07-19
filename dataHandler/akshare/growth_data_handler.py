import pandas as pd

import configger
from mathUtils.average import findWeightAverage
from mathUtils.general import is_all_above_zero, findMax, find_max
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
    engine = configger.getEngine()
    sql = configger.all_growthSQL
    if (code == ''):
        data = pd.read_sql(sql=sql, con=engine)
    recent_data = data.groupby('code').apply(lambda x: getRecnetN(x, n))
    recent_data.index.names = ['code', 'index']
    recent_data.reset_index(inplace=True)
    recent_data.drop(columns='index', inplace=True)
    print(recent_data)
    return recent_data


def select_forecat_report_data()->pd.DataFrame:
    def find_net_profit(x):
        if (x['预测指标'].find('净利润') > 0 and (x['code'].find('sh')>=0 or x['code'].find('sz')>=0)):
            return True
        else:
            return False
    # pd.set_option('display.max_columns', 50)
    engine=configger.getEngine()
    sql='SELECT * FROM tb_ak_bi_forecast_report where date =(select max(date) from tb_ak_bi_forecast_report)'
    data=pd.read_sql(sql=sql,con=engine)[['code','date','预测指标','业绩变动幅度']]
    data=data.loc[data.apply(lambda x:find_net_profit(x),axis=1)]
    data=data.groupby('code').apply(lambda x:find_max(x,column='业绩变动幅度'))
    data.reset_index(drop=True, inplace=True)

    return data
def get_weight_average(data,sort_column='date',value_column='净利润-季度环比增长',n=12,is_above_zero=True,forecast=False):
    if(value_column=='净利润-同比增长' and forecast==True):
        n=n+1
        extendData=select_forecat_report_data()
        extendData.dropna(subset=['业绩变动幅度'],inplace=True)

        extendData=extendData[['code','业绩变动幅度','date']]
        extendData.rename(columns={'业绩变动幅度':'净利润-同比增长'},inplace=True)
        print(extendData)
        data=data.append(extendData)
    print(data)
    print(n)
    # data.groupby('code').apply(lambda x: print(x[value_column].count()))
    is_all=data.groupby('code').apply(lambda x: x[value_column].count() == n)
    is_all=is_all[is_all==True]
    tmp=data.loc[data['code'].isin(is_all.index)]
    # last_date=tmp.groupby('code').apply(lambda x:x[sort_column].min()).max()


    valuecounts=tmp.groupby('code').apply(lambda x:x[sort_column].min()).value_counts()
    last_date=valuecounts.nlargest(1).index[0]

    res = tmp.groupby('code').apply(lambda x: findWeightAverage(x, sort_column=sort_column,value_column=value_column,n=n,last_date=last_date))
    if(is_above_zero==True):
        # print(data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column)))
        res.index.names=['code','index']
        res.reset_index(inplace=True)
        res.set_index('code',inplace=True)
        res.drop('index',inplace=True,axis=1)
        res['is_above_zero']=data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column))
        tmp=data.groupby('code').apply(lambda x:is_all_above_zero(x,value_column))
        res=res.loc[res['is_above_zero']]
    print(res)
    return res

select_forecat_report_data()