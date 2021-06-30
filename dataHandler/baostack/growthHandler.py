import math
from math import e
import pandas as pd
import database
from dataHandler.baostack import marketHandler
from dataHandler.baostack.industryHandler import getIndustryData
from utils.pdUtil import deleteNullColumn, fillNullColumn
def getRecnetN(x,n):
    x.reset_index(inplace=True)
    x.drop(columns=['code'],inplace=True)
    x.sort_values(by=['date'],ascending=False,inplace=True)
    x=x[0:n]
    fillNullColumn(x,'净利润',0)
    return x
def getRecentGrowth(code='',n=1):
    database.init()
    growthSQl=database.growthSQl
    data=pd.read_sql(sql=growthSQl,con=database.mysql,index_col='code')
    print(data)
    data=data.groupby(data.index).apply(lambda x:getRecnetN(x,n))
    data.index.names=['code','index']
    data.reset_index(inplace=True)
    data.set_index('code',drop=True,inplace=True)
    return data

def findAverage(x,n=12):
    # print(x)
    x.reset_index(inplace=True)
    x.sort_values(by=['date'],ascending=False,inplace=True)
    x=x[0:n]
    result=pd.Series(dtype=float)
    x.dropna(subset=['净利润'],inplace=True)


    x['净利润']=x['净利润'].map(lambda x:float(x))
    result['average']=x['净利润'].mean()
    # result['净资产']=x['净资产'].mean()
    # result['总资产']=x['总资产'].mean()
    return result
def findWeightAverage(x,n=12,t=1):
    index=x.index[0]
    x=x.copy()
    # print('x')
    # print(x)
    x.sort_values(by=['date'],ascending=False,inplace=True)
    # print(x)
    x=x[0:n]
    x.reset_index(inplace=True)
    fillNullColumn(x,'净利润',0)
    # x=deleteNullColumn(x,'净利润')
    x=x[['净利润','date']]
    # print(x)
    profit=pd.Series(dtype=float)
    weight=pd.Series(dtype=float)
    result=pd.DataFrame()
    n=len(x)
    # print('x')
    # print(x)
    for i in range(0,n):
        date=x.loc[i,'date']
        weight.loc[date]=float(math.pow(e,-i*t))
        profit.loc[date]=float(x.loc[i,'净利润'])
        result.loc[index,date]=float(x.loc[i,'净利润'])
    weightAverage=(weight*profit).sum()/weight.sum()
    result.loc[index,'weightAverage']=weightAverage
    return result


def findAboveZero(x, times):
    x=x.copy()
    x.sort_values(by=['date'],ascending=False,inplace=True)
    x=x[0:times]
    n=len(x)
    x['净利润'].dropna(0,inplace=True)
    x=deleteNullColumn(x,'净利润')
    x['净利润']=x['净利润'].map(lambda x :float(x))
    count=x['净利润']>0
    return count.sum()
def constantGrowth(codes='all',times=8,allAbove=True,accumulate=False,WeightAccumulate=False):
    database.init()
    growthSQl=database.growthSQl
    data=pd.read_sql(sql=growthSQl,con=database.mysql,index_col='code')
    data.dropna(subset=['净利润'],inplace=True)
    # data.astype({'净利润':'float64'}).dtypes
    # 好好检查一下自己的字符串内容，注意里面是否有换换行符 \n，制表符 \t 或空字符串 ‘ ’ todo
    print(data)
    if(codes!='all'):
        isIn=data.index.isin(codes)
        data=data.loc[isIn]
    above=data.groupby(data.index).apply(lambda x:findAboveZero(x,times))
    print(above)
    above=pd.DataFrame(above)
    above.columns=['above']
    if(allAbove==True):
        res=above==times
        print('res')
        print(res)
        res=res.loc[res['above']==True]
        data=data.loc[data.index.isin(res.index)]
        above=above.loc[above.index.isin(res.index)]
        print('data')
        print(data)
    weightAverageData=data.groupby(data.index,as_index=False).apply(lambda x:findWeightAverage(x,times))

    print(weightAverageData)
    weightAverageData.index.names=['num','code']
    weightAverageData.reset_index(inplace=True)
    weightAverageData.set_index('code',inplace=True,drop=True)
    weightAverageData.drop(columns=['num'],inplace=True)
    print('weightAverageData')
    print(weightAverageData)

    print('above')
    print(above)
    result=pd.concat([weightAverageData,above],axis=1)
    print(result)
    result.dropna(how='any',axis=1,inplace=True)
    result.dropna(how='all',axis=0,inplace=True)
    result.sort_values(by=['above','weightAverage'],inplace=True,ascending=False)

    return result
def chooseByInDustry(times,lowTh=100,highTh=1000):
    res=constantGrowth(codes='all',times=times)
    marketvalue= marketHandler.getmarketValue(lowTh=lowTh, highTh=highTh)
    res=res.loc[res.index.isin(marketvalue.index)]
    industry=getIndustryData()[['code','行业']]
    res=pd.merge(left=res,right=industry,left_index=True,right_on='code')
    res.set_index('code',inplace=True)
    return res
if __name__=='__main__':
    res=chooseByInDustry()
    print(res)