import pandas as pd

import configger
from utils.util import getAllMarketValue
def getmarketValue(data=None,highTh=None,lowTh=None):
    billion=100000000
    sql='select code,totalmarketvalue,liquidmarketvalue from tb_basic_information'
    if(highTh!=None or lowTh!=None):
        sql+=' where'
        list=[]
        if(highTh!=None):
            highTh=highTh*billion
            list.append(' totalmarketvalue < {}'.format(highTh))
        if(lowTh!=None):
            lowTh=lowTh*billion
            list.append(' totalmarketvalue > {}'.format(lowTh))
        sql+= ' and'.join(list)
    print(sql)
    configger.init()
    engine=configger.engine
    res=pd.read_sql(con=engine,sql=sql,index_col='code')
    if(data!=None):
        try:
            if(data.index=='code'):
                res=res.loc[res.index.isin(data.index)]
            elif('code' in(data.columns.tolist())):
                res=res.loc[res.index.isin(data['code'])]
        except:
            print(res.index.isin(data))
            res=res.loc[res.index.isin(data)]
    return res
if __name__=='__main__':
    a=[1]
    b=2
    res=getmarketValue(['sh.600004'],lowTh=100)
    print(res)