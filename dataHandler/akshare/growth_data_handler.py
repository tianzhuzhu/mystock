import datetime

import pandas as pd

import configger
from mathUtils.average import findWeightAverage
from mathUtils.general import is_all_above_zero, findMax, find_max
from utils import timeUtil
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




def select_forecat_report_data(date='')->pd.DataFrame:
    def find_net_profit(x):
        if (x['预测指标'].find('净利润') > 0 and (x['code'].find('sh')>=0 or x['code'].find('sz')>=0)):
            return True
        else:
            return False
    # pd.set_option('display.max_columns', 50)
    engine=configger.getEngine()

    if(date==''):
        date = datetime.datetime.now().date()
        sql='SELECT * FROM tb_ak_bi_forecast_report where date ="{}"'.format(timeUtil.get_last_end_quarter_day(date))
    else:
        sql = 'SELECT * FROM tb_ak_bi_forecast_report where date ="{}"'.format(date)
    print(sql)
    data=pd.read_sql(sql=sql,con=engine)[['code','date','预测指标','业绩变动幅度','预测数值']]
    data=data.loc[data.apply(lambda x:find_net_profit(x),axis=1)]
    data=data.groupby('code').apply(lambda x:find_max(x,column='业绩变动幅度'))
    data.reset_index(drop=True, inplace=True)
    data.dropna(subset=['code'],inplace=True)
    return data
def get_weight_average(data,sort_column='date',value_column='净利润-季度环比增长',n=12,is_above_zero=True,forecast=False):
    if(value_column=='净利润-同比增长' and forecast==True):
        n=n+1
        extendData=select_forecat_report_data()
        extendData.dropna(subset=['业绩变动幅度'],inplace=True)
        extendData=extendData[['code','业绩变动幅度','date']]
        extendData.rename(columns={'业绩变动幅度':'净利润-同比增长'},inplace=True)
        print('extendData')
        print(extendData)
        extendData.to_excel('a.xlsx')
        data=data.append(extendData)
    print(data)
    print(n)

    is_all=data.groupby('code').apply(lambda x: x[value_column].count() == n)
    print(is_all)
    is_all=is_all[is_all==True]
    tmp=data.loc[data['code'].isin(is_all.index)]
    # last_date=tmp.groupby('code').apply(lambda x:x[sort_column].min()).max()
    print('tmp',tmp)
    if(tmp.index.name=='code' and 'code' in tmp.columns.tolist()):
        tmp.drop(columns='code',inplace=True)
    valuecounts=tmp.groupby('code').apply(lambda x:x[sort_column].min()).value_counts()
    last_date=valuecounts.nlargest(1).index[0]
    print(tmp)
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
def get_last_season_net_profit():
    engine=configger.getEngine()
    lastquater=timeUtil.get_last_end_quarter_day(datetime.datetime.now().date())
    last_two_quater=timeUtil.get_last_end_quarter_day(lastquater)


    print(lastquater,last_two_quater,timeUtil.get_this_end_quarter_day(lastquater.replace(day=1,month=1)))
    last_data=select_forecat_report_data(lastquater)
    last_two_data = pd.read_sql('select *  from tb_ak_bi_yjbb where date="{}"'.format(last_two_quater.date()),con=engine)
    last_two_data=last_two_data[['code','净利润-净利润']]
    print(last_data)
    print(last_two_data)
    last_data = pd.merge(left=last_data, right=last_two_data, how='inner')
    if(lastquater!=timeUtil.get_this_end_quarter_day(lastquater.replace(day=1,month=1))):
        #todo 预测数值单季度计算
        last_data['净利润']=last_data['预测数值']-last_two_data['净利润-净利润']
        
        # last_data['净利润']=last_data['预测数值']-last_two_data['预测数值']
    else:
        last_data['净利润'] = last_data['预测数值']
    last_data['净利润同比增长率']=(last_data['净利润']-last_two_data['净利润-净利润'])/last_two_data['净利润-净利润']
    # print(last_data[['code','净利润','净利润环比增长率']])
    last_data.to_excel('a.xlsx')
    return last_data
get_last_season_net_profit()
# select_forecat_report_data()