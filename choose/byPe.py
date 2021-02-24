import datetime
import random
import time

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import pymysql

if __name__ == '__main__':
    n=200
    sql='select * from todayStock'
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    todayList = pd.read_sql(con=engine, sql=sql)
    todayList['roe']=todayList['pb']/todayList['per']
    print(todayList[['code','per','pb','roe']])
    datalist1=todayList.sort_values(by='per')
    datalist1=datalist1.loc[datalist1['per']>0]
    datalist1=datalist1[:n]
    datalist2=todayList.sort_values(by='pb')
    datalist2 = datalist2[:n]
    datalist3=todayList.loc[todayList['roe'] > 0]
    datalist3.sort_values(by='roe',ascending=False,inplace=True)

    datalist3 = datalist3[:n]
    print(datalist1['code'].isin(datalist2['code']))
    datalist1=datalist1.loc[datalist1['code'].isin(datalist2['code'])]
    print(datalist1['code'].isin(datalist3['code']))
    datalist1=datalist1.loc[datalist1['code'].isin(datalist3['code'])]
    print(datalist1)