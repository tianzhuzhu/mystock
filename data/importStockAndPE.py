import _thread
import datetime
import math
import threading
import time
import traceback
from  tqdm import tqdm
import baostock as bs
import pandas as pd
from sqlalchemy import create_engine

#### 登陆系统 ####
from utils import util


def importBycode(code,start_date,end_date,table,engine,lg):

    # 显示登陆返回信息
    # print('import data',code,start_date,end_date)
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST,peTTM,pbMRQ,psTTM,pcfNcfTTM",
                                  start_date=start_date, end_date=end_date,
                                  frequency="d", adjustflag="3")

    # print('query_history_k_data_plus respond error_code:'+rs.error_code)
    # print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    # print(result)
    result['updateTime']=datetime.datetime.now()
    result.to_sql(table,con=engine,if_exists='append',index=False)
    updateDate=['']
    return result
def importHistory(data,table):
    today = datetime.datetime.now()
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    lg = bs.login()
    i=0
    symbols = tqdm(data['symbol'])
    for symbol in symbols:

        i=i+1
        code=util.getdotCodeBysymbol(symbol)
        nowtime=datetime.datetime.now()
        try:
            sql = 'select max(updateTime) from {} where code="{}"'.format(table, code)
            updateTime = pd.read_sql(sql, con=engine).iloc[0, 0]
            if((nowtime-updateTime).seconds<7200):
                print(symbol,'数据已更新')
                continue
        except:
            # traceback.print_exc()
            pass
        try:
           sql='select max(date) from {} where code="{}"'.format(table,code)

           start_date=pd.read_sql(sql,con=engine).iloc[0,0]
           start_date=pd.to_datetime(start_date)+datetime.timedelta(days=1)
           start_date=start_date.strftime('%Y-%m-%d')
           # start_date=start_date.date()
        except:
           start_date='1990-01-01'
           # traceback.print_exc()
        end_date=today.strftime('%Y-%m-%d')
        # print(start_date,end_date)
        if(start_date>end_date):
            print(code,start_date,'已存在')
            continue
        result=importBycode(code,start_date,end_date,table,engine ,lg)
        if(i%200==0):
            bs.logout()
            time.sleep(2)
            bs.login()

        symbols.set_description("查询代码为：{},数据条数为{}".format(code,len(result.index)))
    bs.logout()

def importTodayStockAndPE():

    data=util.todayStockData()
    threadlist=[]
    try:
        # count= len(data)
        # print('count',count)
        # for i in range(0,10):
        #     slice=count/10
        #     low=math.floor(slice*i)
        #     high=math.ceil(slice*(i+1))
        #
        #     high=count if high >=count else high
        #     print(low, high,count)
        #     tempdata=data.iloc[low:high]
        #     t = threading.Thread(target=importHistory,args=(tempdata,'tb_stock_hisotry_detatil',))
        #     threadlist.append(t)
        # for t in threadlist:
        #     t.setDaemon(True)  # 设置为守护线程，不会因主线程结束而中断
        #     t.start()
        #     # t.join()  # 子线程全部加入，主线程等所有子线程运行完毕
        # time.sleep(1000)
        # # _thread.start_new_thread(importHistory, (data,))
        importHistory(data, 'tb_stock_hisotry_detatil')
        # importHistory(data, 'tb_test1')
    except:
        traceback.print_exc()

if __name__ == '__main__':
    importTodayStockAndPE()