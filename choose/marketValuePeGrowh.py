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

def getRecentDataBydata(data):
    database.init()
    engine=data.engine
    if(data.index.name!='code'):
        data.set_index('code',inplace=True)
    codes=data.index.tolist().join('.')
    sql="select t.* from (" \
        "SELECT max(date) as date,code  FROM tb_stock_hisotry_detatil  e where code in " \
        "({}) GROUP BY code)o ,  tb_stock_hisotry_detatil t where t.code=o.code and t.date=o.date".format(codes)
    result=pd.read_sql(sql=sql,con=engine,index_col='col')
    result=pd.concat([data,result])
    print(result)

def findGrowhBydata(data):
    if(data.index.name!='code'):
        data.set_index('code',inplace=True)
    findGrowhBydata(data)

if __name__ == '__main__':
    data=util.findDataBymarkevalueTH(1000)
    data=findGrowhBydata(data)
    result=getRecentDataBydata(data)
    print(result)
##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



