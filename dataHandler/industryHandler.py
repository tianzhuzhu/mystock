import pandas as pd

import database
from data.importIndustry import UpdateIndustryData


def getIndustryData(code='',date='',index=True):
    result=UpdateIndustryData()
    if(not result.empty and code!=''):
        return result
    if(code==''):
        database.init()
        indutrysql=database.industrySQL
        print(indutrysql)

        if(index):
            data=pd.read_sql(sql=indutrysql,con=database.engine,index_col='code')
        else:
            data=pd.read_sql(sql=indutrysql,con=database.engine)
    else:
        database.init()
        if(index):
            indutrysql=database.industrySQL2
            data=pd.read_sql(sql=indutrysql.format(code),con=database.engine,index_col='code')
        else:
            indutrysql=database.industrySQL2
            data=pd.read_sql(sql=indutrysql.format(code),con=database.engine)
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
