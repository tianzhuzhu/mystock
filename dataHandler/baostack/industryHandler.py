import pandas as pd

import configger
from data.baostack.importIndustry import UpdateIndustryData


def getIndustryData(code='',date='',index=True):
    result=UpdateIndustryData()
    print('result')
    print(result)
    if(not result.empty and code!=''):
        return result
    if(code==''):
        configger.init()
        indutrysql=configger.industrySQL
        print(indutrysql)

        if(index):
            data=pd.read_sql(sql=indutrysql, con=configger.engine)
        else:
            data=pd.read_sql(sql=indutrysql, con=configger.engine)
    else:
        configger.init()
        if(index):
            indutrysql=configger.industrySQL2
            data=pd.read_sql(sql=indutrysql.format(code), con=configger.engine, )
        else:
            indutrysql=configger.industrySQL2
            data=pd.read_sql(sql=indutrysql.format(code), con=configger.engine)
    return data
def findMax(x,column):

    maxprofit=x[column].max()
    code=x.loc[x[column]==maxprofit,'code'].iloc[0]

    print(x.columns.tolist())
    data=pd.DataFrame(columns=x.columns.tolist())
    data.index.name=code
    data.loc[code]=x.loc[x[column]==maxprofit].iloc[0]
    # print(data)
    return data

    return res
