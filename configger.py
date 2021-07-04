import datetime
import os

from sqlalchemy import create_engine
import logging
import utils.loadData
from utils.sqlUtil import getsql


def init():
    global engine, path, date, data, mysql
    global lastOperateTimeSql, cur_path
    global growthSQl, marketSQl, industrySQL, industrySQL2, peSQL
    dirname, filename = os.path.split(os.path.abspath(__file__))
    global all_growthSQL
    global constant_variables
    cur_path=dirname
    # print(dirname)

    lastOperateTimeSql="select max(updateTime) from tb_operation_time where name='{}'"
    data=utils.loadData.loadData('config.yml')
    growthSQl=getStrSQL('growth')
    industrySQL=getStrSQL('industrySQL')
    industrySQL2=getStrSQL('industrySQL2')
    peSQL=getStrSQL('peSQL')
    all_growthSQL=getStrSQL('akshare_all_growth')
    date=datetime.datetime.now().date()
    engine=create_engine(data['db'])
    constant_variables=data['constant_variables']
    mysql=engine
    path=r'选股\KLine\{}'.format(date)
def getStrSQL(sql):
    sql=data['sql'][sql]
    sql=os.path.join(cur_path,sql)
    sql=getsql(sql)
    return sql
if __name__=='__main__':
    init()
    print(data)