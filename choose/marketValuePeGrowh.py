import datetime
import os

import database
import myEmail.send
import utils.util as util
import pandas as pd
from sqlalchemy import create_engine

import utils.loadData


def search(x,n):
    x=x[0:n]
    todayvolume=x.loc[x['date'].max()==x['date'],'volume'].iloc[0]
    print(todayvolume)
    x['close']=  x['close'].apply(float)
    avg=x['close'].mean()

    sumv=(x['volume']>todayvolume).apply(int).sum()
    data=x.loc[x['date']==x['date'].max(),['YOYNI','peTTM','pbMRQ','close']]
    data=data.iloc[0]
    # return pd.Series({'sum':sumv,'增长率':data.iloc[0,0],'pe':data.iloc[0,1],'pb':data.iloc[0,2]})
    data['count']=sumv
    data['avg']=data['close']/avg
    return data
# ,'peTTM','pbMRQ'
#阈值单位亿



if __name__ == '__main__':
    data=util.findDataBymarkevalueTH(1000)
    data= util.findGrowhBydata(data)
    result= util.getRecentDataBydata(data)
    print(result)
##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



