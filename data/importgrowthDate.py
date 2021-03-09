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
    return  result_growth


def importData(stockData,engine):

    lg = bs.login()
    year = datetime.datetime.now().year
    for code in stockData['symbol']:
        data=pd.DataFrame()
        print(code)
        code=getCode(code)
        print(code)
        for i in range(2015,year+1):
            for j in range(1,5):
                date=str(i)+'-'+str(j)
                try:
                    sql='select count(1) from tb_growth where date="{}" and code="{}"'.format(date,code)
                    count=pd.read_sql(con=engine,sql=sql)
                    if(count.iloc[0,0]==1):
                        # print(count)
                        continue
                except:
                    traceback.print_exc()
                result=getData(code,i,j)
                result['code']=code
                result['date']=date

                if(data.empty):
                    data=pd.DataFrame(columns=result.columns)
                data=data.append(result,ignore_index=True)
        time.sleep(0.5)
        print(data)
        data.to_sql('tb_growth',con=engine,if_exists='append')
    bs.logout()



def mainProcess():
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
    mainProcess()