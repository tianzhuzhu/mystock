import datetime
import random
import time
import traceback

import akshare as ak
import pandas as pd
import baostock as bs
from sqlalchemy import create_engine

def importData(data,engine):
    keys= {'利润表':'tb_income_statement','资产负债表':'tb_balance_sheet','现金流量表':'tb_flow_cash'}
    lg = bs.login()
    end_date = datetime.datetime.now().date()
    for code in data['symbol']:
        code=list(code)
        code.insert(2,'.')
        code=''.join(code)
        print(code)
        # 显示登陆返回信息
        # print('login respond error_code:' + lg.error_code)
        # print('login respond  error_msg:' + lg.error_msg)

        #### 获取公司业绩快报 ####

        rs = bs.query_performance_express_report(code, start_date="1990-01-01", end_date='2020-12-31')
        print('query_performance_express_report respond error_code:' + rs.error_code)
        print('query_performance_express_report respond  error_msg:' + rs.error_msg)

        result_list = []
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
            # 获取一条记录，将记录合并在一起
        result = pd.DataFrame(result_list, columns=rs.fields)
        #### 结果集输出到csv文件 ####
        # result.to_csv("D:\\performance_express_report.csv", encoding="gbk", index=False)
        # print(result)

        result.to_sql('performance',con=engine,if_exists='append')
        time.sleep(0.1)
        #### 登出系统 ####
    bs.logout()
        # for k,v in keys.items():
        #     try:
        #         result = ak.stock_financial_report_sina(stock=code, symbol=k)
        #         result['code']=code
        #
        #         # Balance sheet Cash flow statement Income statement
        #         sql='select * from {} where code ={}'.format(v,code)
        #         data = pd.read_sql(con=engine, sql=sql)
        #         result=ak.stock_financial_report_sina(stock=code, symbol=k)
        #         result=result.loc[result['报表日期'].isin[data['报表日期']]]
        #
        #     except:
        #         result=ak.stock_financial_report_sina(stock=code, symbol=k)
        #     print(result)
        #     try:
        #         result.to_sql(v, con=engine, if_exists='append')
        #     except:
        #         # traceback.print_exc()
        #         pass
        # time.sleep(random(5,20))

def mainProcess():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    createTimeSql = " SELECT CREATE_TIME from information_schema.`TABLES`  WHERE  `information_schema`.`TABLES`.`TABLE_SCHEMA` = 'stock' and `information_schema`.`TABLES`.`TABLE_NAME` = 'todaystock' "

    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    createTime = pd.read_sql(con=engine, sql=createTimeSql)
    if (datetime.datetime.now().day != createTime.iloc[0, 0].day):
        stockData = ak.stock_zh_a_spot()
        stockData.to_sql('todaystock', con=engine, if_exists='replace')
    else:
        stockData = pd.read_sql(con=engine, sql='select * from todayStock')
    importData(stockData,engine)
if __name__=='__main__':
    mainProcess()