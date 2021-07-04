import pandas as pd

from utils.pdUtil import deleteNullColumn


def is_all_above_zero(x,column):
    x=x.copy()
    n=len(x)
    x[column].fillna(0,inplace=True)
    x=deleteNullColumn(x,column)
    x[column]=x[column].map(lambda x :float(x))
    count=x[column]>0
    if(count.sum()==n):
        return True
    else:
        return False

def findMax(x,column):

    maxprofit=x[column].max()
    code=x.loc[x[column]==maxprofit,'code'].iloc[0]
    data=pd.DataFrame(columns=x.columns.tolist())
    data.index.name=code
    data.loc[code]=x.loc[x[column]==maxprofit].iloc[0]
    # print(data)
    return data
