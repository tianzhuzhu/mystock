import datetime
import os
import time
import traceback
import akshare as ak
import baostock as bs
import pandas as pd
from tqdm import tqdm
# 登陆系统
from sqlalchemy import create_engine

import configger
from utils import util
from utils.util import todayStock


def queryByCode(code,year,season):
    # 查询季频估值指标盈利能力
    profit_list = []
    rs_profit = bs.query_profit_data(code=code, year=year, quarter=season)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    # 打印输出
    # print(result_profit)
    return result_profit
    # 结果集输出到csv文件
def importData(stockData,engine):
    i,count =0, len(stockData.index)

    lg = bs.login()
    toyear = datetime.datetime.now().year
    toseason=int(datetime.datetime.now().month/4)+1
    codes = tqdm(stockData['symbol'])
    for code in codes:
        # print(code)
        data=pd.DataFrame()
        # print(code)
        # print(code)
        now=datetime.datetime.now()
        sql='select max(updateTime) from tb_profit where  code="{}"'.format(code)
        try:

            updateTime=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            if(now-updateTime).seconds>7200:
                continue
        except:
            pass
        sql='select max(date) from tb_profit where  code="{}"'.format(code)
        i=i+1
        try:
            date=pd.read_sql(con=engine,sql=sql).iloc[0,0]
            year,season=date.split('-')
            year,season=int(year),int(season)
        except:
            year=1989
            season=4

        season=season+1
        year =year+1 if(season==5) else year
        season =0 if(season==5) else season
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
        for i in list:
            date=str(int(i/10))+'-'+str(i%10)
            try:
                result=queryByCode(code,int(i/10),i%10)
                result['code']=code
                result['date']=date

                if(data is None or data.empty):
                    data=result
                else:
                    data=data.append(result,ignore_index=True)
                    # print(count)
            except:
                traceback.print_exc()
        # time.sleep(0.5)
        # print(data)
        data['updateDate']=datetime.datetime.now()
        data.to_sql('tb_profit',con=engine,if_exists='append',index=False)
        # print(stockData)
        bar = stockData['symbol']
        # progress_bar = tqdm(bar)
        os.system('cls')
        if(i%200==0):
            bs.logout()
            time.sleep(5)
            bs.login()
        codes.set_description("导入利润表中代码为{},条数为{}".format(code,len(data.index)))
        # with tqdm(total=count) as pbar:
        #     print(i)

        #     pbar.update(i)
        # i = i + 1
    bs.logout()
def importProfit():
    configger.init()
    engine=configger.engine
    stockData=todayStock()
    importData(stockData,engine)
if __name__ == '__main__':
    importProfit()