import traceback
from datetime import datetime

import baostock as bs
import pandas as pd

# 登陆系统
import database
from utils.util import needUpdate


def inportIndustryData(name='tb_today_industry',code=None,date=None):
    database.init()
# 显示登陆返回信息

    # 结果集输出到csv文件

    con=database.engine
    try:
        sql=database.lastOperateTimeSql.format(name)
        lastTime=pd.read_sql(sql=sql,con=con).iloc[0,0]
        print(lastTime)
    except:
        print('没有操作数据')
    if(lastTime==None):
        lastTime=pd.to_datetime('1990-1-1 00:00:00')


    if(needUpdate(lastTime,datetime.now(),True)==True):
        lg = bs.login()
        # 获取行业分类数据
        rs = bs.query_stock_industry()

    # rs = bs.query_stock_basic(code_name="浦发银行")

    # 打印结果集
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            industry_list.append(rs.get_row_data())
        result = pd.DataFrame(industry_list, columns=rs.fields)
        result['date']=datetime.now().date()

        result.to_sql(name=name,con=con,if_exists='append',index=False)
        bs.logout()
        operation=pd.DataFrame()
        operation.loc[0,'name']=name
        operation.loc[0,'updateTime']=datetime.now().date()
        operation.to_sql(name='tb_operation_time',con=con,if_exists='append',index=False)
        print('industry_data_import_ok')
    else:
        print('无需插入')
# 登出系统

if __name__=='__main__':
    inportIndustryData()