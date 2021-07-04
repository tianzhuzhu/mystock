import pandas as pd

import configger
from dataHandler.akshare.growth_data_handler import select_growth_data, get_weight_average
from dataHandler.baostack import marketHandler
from mathUtils.average import findWeightAverage
from mathUtils.general import findMax
from utils.pdUtil import getRecnetN
def select_all_CI(key):#key : 行业/概念
    configger.init()
    con=configger.engine
    if(key=='概念'):
        sql='select * from tb_ak_concept_infos where convert(update_time,date)=convert((select max(update_time) from tb_ak_concept_infos),date)'
    if (key == '行业'):
        sql = 'select * from tb_ak_industry_infos where convert(update_time,date)=convert((select max(update_time) from tb_ak_industry_infos),date)'
    data=pd.read_sql(sql=sql,con=con,index_col='序号')
    data.rename(columns={'代码':'code'},inplace=True)
    return data
def cocept_weight_average(n=6,value_column='净利润-季度环比增长',is_above_zero=True,key='概念'):
    data=select_all_CI(key)[['code','名称',key]]
    print(key)
    print(data)
    growth_data=select_growth_data(n=n)
    marketvalue= marketHandler.getmarketValue(lowTh=200, highTh=20000)
    data=data.loc[data['code'].isin(marketvalue.index)]
    res=get_weight_average(growth_data,value_column=value_column,n=n,is_above_zero=is_above_zero)
    data=pd.merge(on='code',left=data,right=res,validate='many_to_many')
    res=data.groupby(key).apply(lambda x:findMax(x,column='weightAverage'))
    res.sort_values('weightAverage',inplace=True,ascending=False)
    res.drop(columns=['code',key,'is_above_zero'],inplace=True)
    res.to_excel(key+'.xlsx')
    return res

cocept_weight_average()
cocept_weight_average(key='行业')