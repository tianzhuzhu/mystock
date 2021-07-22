import os

import pandas as pd

import configger
from dataHandler.akshare.growth_data_handler import select_growth_data, get_weight_average, select_forecat_report_data
from dataHandler.baostack import marketHandler
from mathUtils.average import findWeightAverage
from mathUtils.general import findMax, find_top_n
from myEmail.send import send_file_email
from utils.excelUtil import save_excel
from utils.pdUtil import getRecnetN
def select_all_CI(key):#key : 行业/概念
    configger.init()
    con=configger.engine
    if(key=='概念'):
        sql='select * from tb_ak_concept_infos where convert(update_time,date)=convert((select max(update_time) from tb_ak_concept_infos),date)'
    if (key == '行业'):
        sql='select * from tb_ak_industry_infos where convert(update_time,date)=convert((select max(update_time) from tb_ak_industry_infos),date)'
    data=pd.read_sql(sql=sql,con=con,index_col='序号')
    data.rename(columns={'代码':'code'},inplace=True)
    return data
def cocept_weight_average(n=4,value_column='净利润-季度环比增长',is_above_zero=True,key='概念',forecast=False):
    data=select_all_CI(key)[['code','名称',key]]
    print(key)
    print(data)
    growth_data=select_growth_data(n=n)
    print()
    marketvalue= marketHandler.getmarketValue(lowTh=50, highTh=20000)
    data=data.loc[data['code'].isin(marketvalue.index)]
    res=get_weight_average(growth_data,value_column=value_column,n=n,is_above_zero=is_above_zero,forecast=forecast)
    print(res)
    data=pd.merge(on='code',left=data,right=res,validate='many_to_many')
    print(data)
    if(key=='概念'):
        res=data.groupby(key).apply(lambda x:findMax(x,column='weightAverage'))
    else:
        res = data.groupby(key).apply(lambda x: find_top_n(x, column='weightAverage'))
    res.sort_values('weightAverage',inplace=True,ascending=False)
    res.drop(columns=[key,'is_above_zero'],inplace=True)
    print(res)
    # res.to_excel(name)
    return res

def cocept_forecast_report(value_column='净利润-季度环比增长',key='概念'):
    data=select_all_CI(key)[['code','名称',key]]

    res=select_forecat_report_data()
    marketvalue= marketHandler.getmarketValue(lowTh=50, highTh=20000)
    data=data.loc[data['code'].isin(marketvalue.index)]
    print('data')
    print(data)
    data=pd.merge(on='code',left=data,right=res,validate='many_to_many')
    print(data)
    if(key=='概念'):
        res=data.groupby(key).apply(lambda x:findMax(x,column='业绩变动幅度'))
    else:
        res = data.groupby(key).apply(lambda x: find_top_n(x, column='业绩变动幅度'))
    res.sort_values('业绩变动幅度',inplace=True,ascending=False)
    # res.drop(columns=[key],inplace=True)
    # res.to_excel('预告排序-'+key+value_column+'.xlsx')
    return res


def get_weight_average_data():

    a1=cocept_weight_average()
    a2=cocept_weight_average(value_column='营业收入-季度环比增长',n=4)
    a3=cocept_weight_average(value_column='净利润-同比增长',n=4)
    a4=cocept_weight_average(value_column='净利润-同比增长',n=4,forecast=True)
    a5=cocept_weight_average(key='行业')
    a6=cocept_weight_average(key='行业',value_column='营业收入-季度环比增长')
    a7=cocept_weight_average(key='行业',value_column='净利润-同比增长',n=4)
    a8=cocept_weight_average(key='行业',value_column='净利润-同比增长',n=4,forecast=True)
    a9=cocept_forecast_report()
    a10=cocept_forecast_report(key='行业')
    res={'概念-净利润-季度环比增长':a1,
         '概念-营业收入-季度环比增长':a2,
         '概念-净利润-同比增长':a3,
         '概念-业绩预告净利润-同比增长':a4,
         '行业-净利润-季度环比增长': a5,
         '行业-营业收入-季度环比增长': a6,
         '行业-净利润-同比增长': a7,
         '行业-业绩预告净利润-同比增长': a8,
         '概念-预告最高': a9,
         '行业-与该最高': a10,
    }

    return res
def save_top():
    cocept_forecast_report()
    cocept_forecast_report(key='行业')


if __name__=='__main__':
    res=get_weight_average_data()
    path=os.path.join(configger.default_save_path,'概念-业绩报告.xlsx')
    save_excel(path,res)
    send_file_email('概念-业绩报告.xlsx',path)