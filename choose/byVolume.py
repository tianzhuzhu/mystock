import datetime
import os
import random
import time

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import traceback

import utils.util

def getVolumes(symbols,k,countDays):
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    sql='select * from todayStock'
    todayData=pd.read_sql(con=engine,sql=sql)
    rows=[]
    for i in symbols:
        # print(i)
        sql='select * from stockHistory where symbol="{}"  order by date desc limit 0,{}'.format(i,countDays)
        data=pd.read_sql(con=engine,sql=sql)
        try:


            if(data['close'].iloc[0]<=k *(data['close'].mean())):
                today=(todayData.loc[todayData['symbol']==i]).iloc[0]
                print(today)
                if(today['per']<=20 and today['per']>0):
                    todayvolume=data['volume'].iloc[0]
                    # print('todayVolume',todayvolume)
                    roe=today['pb']/today['per']
                    # print('roe',roe)
                    sel=todayvolume<data['volume']
                    values=sel.value_counts()
                    rows.append({'symbol':i,'count':values.loc[True],'roe':roe,'pe':today['per']})
        except:
            traceback.print_exc()
        # print(rows)
    result=pd.DataFrame.from_dict(rows)
    print(result)
    return result

def SortValueByvolume(countDays,k):
    sql='select * from todayStock'
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    todayData=pd.read_sql(con=engine,sql=sql)
    rows=[]
    symbols=todayData['symbol']
    result=getVolumes(symbols,k=0.8,countDays=100)
    # print(result)
    return result
def choose(count=40,k=0.8):
    try:
        result=SortValueByvolume(count,k)
        print(result)
        result.sort_values(by=['count','pe'],inplace=True,ascending=[False,True])
        date=datetime.date.today()
        result=result[0:10]

        path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\volume\{}'.format(date)
        if(not os.path.exists(path)):
            os.mkdir(path)
        result.rename(columns={'symbol':'code'},inplace=True)
        result['code']=result['code'].map(lambda x:utils.util.getdotCodeBysymbol(x))

        resultpath=os.path.join(path,'byvolume.xlsx')
        if(not os.path.exists(resultpath)):
            result.to_excel(resultpath,sheet_name=str(count))
        else:
            with pd.ExcelWriter(resultpath,mode='a') as writer:
                result.to_excel(writer, sheet_name=str(count),index=False)

        engine = create_engine('mysql+pymysql://root:root@localhost:3306/result')

        # result.to_sql('tb'+'-'+str(date),con=engine,if_exists='append')
    except:
        traceback.print_exc()
    return resultpath
def toData(count=40,k=.8):
    date=datetime.date.today()
    path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\volume\{}'.format(date)
    data=chooseToData(count=40,k=0.8,topn=10)
    if(not os.path.exists(path)):
        os.mkdir(path)
    return data
def chooseToData(count=40,k=0.8,topn=10):
    try:
        data=SortValueByvolume(count,k)
        data.sort_values(by=['count','pe'],inplace=True,ascending=[False,True])
        data.rename(columns={'symbol':'code'},inplace=True)
        data['code']=data['code'].map(lambda x:utils.util.getdotCodeBysymbol(x))

        data=data[0:topn]
    except:
        traceback.print_exc()
    return data
if __name__ == '__main__':
    print(toData())
