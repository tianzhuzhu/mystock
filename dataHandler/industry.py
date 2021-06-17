import baostock as bs
import pandas as pd

import database
from data.importIndustry import UpdateIndustryData
from dataHandler.growth import getRecentGrowth
from utils import timeUtil
from utils.timeUtil import tableNeedUpdate, saveOperationTime

def getIndustryData(code='',date=''):
    result=UpdateIndustryData()
    if(not result.empty and code!=''):
        return result
    if(code==''):
        database.init()
        indutrysql=database.industrySQL
        print(indutrysql)
        data=pd.read_sql(sql=indutrysql,con=database.engine)
    else:
        database.init()
        indutrysql=database.industrySQL2
        data=pd.read_sql(sql=indutrysql.format(code),con=database.engine)
    return data
def findMax(x):
    data=pd.DataFrame()
    maxprofit=x['净利润'].max()
    code=x.loc[x['净利润']==maxprofit,'code'].iloc[0]
    data.loc[code,'净利润']=maxprofit
    data.index.name='code'
    # print(data)
    return data
if __name__=='__main__':
    indutry=getIndustryData()
    print(indutry)
    growth=getRecentGrowth(n=1)
    data=pd.merge(left=growth,right=indutry,on='code')
    print(data)
    data['净利润']=data['净利润'].astype(float)
    result=data.groupby('行业')['净利润'].agg('mean')
    result.name='净利润增长率均值'
    print(result)
    result.sort_values(ascending=False,inplace=True)
    print(result)

    data.reset_index(inplace=True)
    result2=data.groupby('行业').apply(lambda x:findMax(x))
    print(result2)
    result2.to_excel('result2.xlsx')