import time
import traceback

import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
# 登陆系统
from utils import util
import datetime
def getData(code,year,quater):

    dupont_list = []
    rs_dupont = bs.query_dupont_data(code=code, year=year, quarter=quater)

    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    # print(code,year,quater)
    # print(result_profit)
    return result_profit
def QuerryDupontData(data,table,engine):

    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)+1
    for code in data['symbol']:
        data=pd.DataFrame()
        print(code)
        # print(code)
        sql='select max(date) from {} where  code="{}"'.format(table,code)
        try:
            date=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            year,month=date.split('-')
            year,month=int(year),int(month)
        except:
            year=1989
            month=12

        # year,month=date.split('-')
        # year,month=int(year),int(month)
        season=int(month/4) +1

        season=season+1
        year =year+1 if(season==5) else year
        season =0 if(season==5) else season+1
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
        print(list)
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            # print(date)
            try:
                result=getData(code,int(i/10),i%10)
                result['code']=code
                result['date']=date

                if(data.empty):
                    # print('result')
                    # print(result)
                    data=result
                else:
                    data=data.append(result,ignore_index=True)
                print(data)
                # print(count)
                # print(data)
            except:
                traceback.print_exc()

        time.sleep(0.5)
        print(data)
        data.to_sql(table,con=engine,if_exists='append')
    bs.logout()
def importAllData():
    data=util.todayStock()
    threadlist=[]
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')

    try:
        QuerryDupontData(data, 'tb_stock_dupont',engine)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    importAllData()