import pandas as pd

import database
from dataHandler.baostack.industryHandler import getIndustryData


def industryPe():
    database.init()
    engine=database.engine
    peSQl=database.peSQL
    print(peSQl)
    industryData=getIndustryData(index=True)
    print(industryData)
    peData=pd.read_sql(con=engine,sql=peSQl,index_col='code')
    data=pd.merge(left=industryData,right=peData,left_index=True,right_index=True,how='inner')
    res=data.groupby('行业')[['peTTM','pbMRQ','psTTM','pcfNcfTTM']].agg('mean')
    print(data)
    print(res)
    return res

def findmin(x,column):
    x.reset_index(inplace=True)
    minpe=x[column].min()
    code=x.loc[x[column]==minpe,'code'].iloc[0]

    print(x.columns.tolist())
    data=pd.DataFrame(columns=x.columns.tolist())
    data.index.name=code
    data.loc[code]=x.loc[x[column]==minpe].iloc[0]
    # print(data)
    return data

def industryMinPE():
    database.init()
    engine=database.engine
    peSQl=database.peSQL
    print(peSQl)
    industryData=getIndustryData(index=True)
    print(industryData)
    peData=pd.read_sql(con=engine,sql=peSQl,index_col='code')
    peData=peData.loc[peData['peTTM']>0]
    data=pd.merge(left=industryData,right=peData,left_index=True,right_index=True,how='inner')
    print(data)
    res=data.groupby('行业').apply(lambda x:findmin(x,'peTTM'))
    return res
if __name__=='__main__':
    industry=industryPe()
    list = ['industry_'+i for i in industry.columns.tolist()]
    industry.columns=list

    instryMinPE=industryMinPE()
    list = ['minPE_'+i for i in instryMinPE.columns.tolist()]
    instryMinPE.columns=list
    res=pd.merge(left=industry,right=instryMinPE,left_index=True,right_index=True)
    print(res)
    res.to_excel('a.xlsx')