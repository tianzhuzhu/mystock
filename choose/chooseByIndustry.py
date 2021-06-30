import pandas as pd

from dataHandler.baostack import growthHandler
from dataHandler.baostack.industryHandler import getIndustryData, findMax


def choose(times=8,lowTh=200,highTh=20000):
    indutry=getIndustryData()
    print(indutry)
    growth= growthHandler.getRecentGrowth(n=1)
    data=pd.merge(left=growth,right=indutry,on='code')
    print(data)
    data['净利润']=data['净利润'].astype(float)
    res=[]
    result=data.groupby('行业')['净利润'].agg('mean')
    result=pd.DataFrame(result)
    result.columns=['净利润']
    result.sort_values(by='净利润',ascending=False,inplace=True)
    print(result)
    print(result)
    res.append(result)
    data.reset_index(inplace=True)
    print(data)
    result2=data.groupby('行业').apply(lambda x:findMax(x,'净利润'))
    print(result2)
    result2.sort_values(by='净利润',ascending=False,inplace=True)
    result2.rename(columns={'level_0':'index'},inplace=True)
    result2.drop(columns=['index','code','所属行业类别','行业','index'],axis=1   )
    print(result2)
    res.append(result2)

    result3= growthHandler.chooseByInDustry(times=times, lowTh=lowTh, highTh=highTh)
    result3.reset_index(inplace=True)
    result3=result3.groupby('行业').apply(lambda x:findMax(x,'weightAverage'))
    result3.sort_values(by='weightAverage',ascending=False,inplace=True)
    result3.drop(columns=['code','行业'],axis=1)
    res.append(result3)
    print(result3)
    for i in res:
        i.dropna(how='any',inplace=True)
    return res