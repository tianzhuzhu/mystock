import datetime
import random
import time

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import traceback
def SortValueByvolume(countDays,k):
    sql='select * from todayStock'
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    rows=[]
    todayData=pd.read_sql(con=engine,sql=sql)
    for i in todayData['symbol']:
        print(i)
        sql='select * from stockHistory where symbol="{}"  order by date desc limit 0,{}'.format(i,countDays)
        data=pd.read_sql(con=engine,sql=sql)
        try:

            if(data['close'].iloc[0]<=k *(data['close'].mean())):
                today=(todayData.loc[todayData['symbol']==i]).iloc[0]
                if(today['per']<=20 and today['per']>0):
                    todayvolume=data['volume'].iloc[0]
                    print('todayVolume',todayvolume)
                    roe=today['pb']/today['per']
                    print('roe',roe)
                    sel=todayvolume<data['volume']
                    values=sel.value_counts()
                    rows.append({'symbol':i,'count':values.loc[True],'roe':roe,'pe':today['per']})
        except:
            traceback.print_exc()
        # print(rows)
    result=pd.DataFrame.from_dict(rows)
    # print(result)
    return result

if __name__ == '__main__':
    result=SortValueByvolume(440,0.7)
    print(result)
    result.sort_values(by=['count','pe'],inplace=True,ascending=[False,True])
    date=datetime.date.today()
    result.to_excel('result{}.xlsx'.format(date))
