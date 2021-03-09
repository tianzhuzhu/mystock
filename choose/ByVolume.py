import datetime
import os
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
    list=[40,90,220,440]
    for count in list:
        try:
            result=SortValueByvolume(count,0.75)
            print(result)
            result.sort_values(by=['count','pe'],inplace=True,ascending=[False,True])
            date=datetime.date.today()
            path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\volume\{}'.format(date)
            if(not os.path.exists(path)):
                os.mkdir(path)
            resultpath=os.path.join(path,'byvolume.xlsx')
            if(not os.path.exists(resultpath)):
                result.to_excel(resultpath,sheet_name=str(count))
            else:
                with pd.ExcelWriter('本地excel文件.xlsx',mode='a') as writer:
                    result.to_excel(writer, sheet_name=str(count),index=False)

            engine = create_engine('mysql+pymysql://root:root@localhost:3306/result')

            result.to_sql('tb'+'-'+str(date),con=engine,if_exists='append')
        except:
            pass
