import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
from sqlalchemy import create_engine
#由600000到 sh.600000
def getCode(code):
    code=list(code)
    code.insert(2,'.')
    code=''.join(code)
    return code
def getData(code,year,quater):
    growth_list = []
    rs_growth = bs.query_growth_data(code=code, year=year, quarter=quater)
    while (rs_growth.error_code == '0') & rs_growth.next():
        growth_list.append(rs_growth.get_row_data())
    result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
    print(result_growth)
    return  result_growth


def importData(stockData,engine):

    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)+1
    for code in stockData['symbol']:
        data=pd.DataFrame()
        print(code)
        code=getCode(code)
        print(code)
        sql='select max(date) from tb_growth where  code="{}"'.format(code)
        try:
            date=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            year,month=date.split('-')
            year,month=int(year),int(month)
        except:
            year=1989
            month=12
        season=int(month/4) +1
        season=season+1
        year =year+1 if(season==5) else year
        season =0 if(season==5) else season+1
        print(year,season)
        list=[]
        for i in range(year,toyear+1):
            for j in range(1,5):
                if(year==i and j>season):
                    list.append(i*10+j)
                elif(i>year and j<=toseason):
                    list.append(i*10+j)
        print(list)
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            print(date)
            try:
                result=getData(code,int(i/10),i%10)
                result['code']=code
                result['date']=date

                if(data.empty):
                    data=pd.DataFrame(columns=result.columns)
                else:
                    data=data.append(result,ignore_index=True)
                    # print(count)
            except:
                traceback.print_exc()

        time.sleep(0.5)
        print(data)
        data.to_sql('tb_growth',con=engine,if_exists='append')
    bs.logout()



def importGrowth():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    createTimeSql = " SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "

    createTime = pd.read_sql(con=engine, sql=createTimeSql)
    if (datetime.datetime.now().day != createTime.iloc[0, 0].day):
        stockData = ak.stock_zh_a_spot()
        stockData.to_sql('todaystock', con=engine, if_exists='replace')
    else:
        stockData = pd.read_sql(con=engine, sql='select * from todayStock')
    importData(stockData,engine)
if __name__=='__main__':
    importGrowth()