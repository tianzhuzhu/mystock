import math

import pandas as pd
from pandas import Period

import configger
from utils.pdUtil import deleteNullColumn


def findWeightAverage(x,n=12,t=configger.T,sort_column='date',value_column='净利润',last_date=''):
    index=x.index[0]
    x=x.copy()
    x.sort_values(by=[sort_column],ascending=False,inplace=True)
    if(last_date!=''):
        x=x.loc[x[sort_column]>=last_date]
    else:
        x=x[0:n]
    x = deleteNullColumn(x, value_column)
    x.reset_index(inplace=True)
    x=x[[value_column,sort_column]]
    profit=pd.Series(dtype=float)
    weight=pd.Series(dtype=float)
    result=pd.DataFrame()
    n=len(x)
    for i in range(0,n):
        date=pd.to_datetime(x.loc[i,sort_column])
        date=Period(date,freq='Q')
        date=date.strftime('%yQ%q')
        column=str(date)+value_column
        weight.loc[column]=float(math.pow(math.e, -i * t))
        profit.loc[column]=float(x.loc[i,value_column])
        result.loc[index,column]=float(x.loc[i,value_column])
    weightAverage=(weight*profit).sum()/weight.sum()
    result.loc[index,'weightAverage']=weightAverage
    return result