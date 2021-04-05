import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
from sqlalchemy import create_engine
#由600000到 sh.600000
from tqdm import tqdm

from utils.util import todayStock


def getData(code,year,quater):
    growth_list = []
    rs_growth = bs.query_growth_data(code=code, year=year, quarter=quater)
    while (rs_growth.error_code == '0') & rs_growth.next():
        growth_list.append(rs_growth.get_row_data())
    result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
    # print(result_growth)
    return  result_growth
def importData(stockData,engine):
    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)+1
    i=0
    codes = tqdm(stockData['symbol'])
    for code in codes:

        sql='select max(date) from tb_growth where  code="{}"'.format(code)
        try:
            Lastdate=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            year,season=Lastdate.split('-')
            year,season=int(year),int(season)
        except:
            year=1989
            season=4
        season=season+1
        year =year+1 if(season==5) else year
        season =1 if(season==5) else season
        # print(year,season)
        list=[]
        for i in range(year,toyear+1):
            for j in range(1,5):
                #最后一次数据的年
                if(i==year and j>=season):
                    list.append(i*10+j)
                #今年
                elif(i==toyear and j<=toseason):
                    list.append(i*10+j)
                #中间年
                elif(i>year and i<toyear):
                    list.append(i*10+j)
        # print(list)
        data = pd.DataFrame()
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            # print(date)
            try:
                result=getData(code,int(i/10),i%10)
                # print(result)
                result['code']=code
                result['date']=date
                if(data is None or data.empty):
                    data=result
                else:
                    data=data.append(result,ignore_index=True)

            except:

                traceback.print_exc()
        data.to_sql('tb_growth',con=engine,if_exists='append')

        codes.set_description("导入成长表中代码为{},条数为{}".format(code,len(data.index)))
        if(i%200==0):
            bs.logout()
            time.sleep(5)
            bs.login()
    bs.logout()



def importGrowth():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    stockData=todayStock()
    importData(stockData,engine)
if __name__=='__main__':
    importGrowth()