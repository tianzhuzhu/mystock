import datetime
import os

from sqlalchemy import create_engine
import logging
import utils.loadData
from utils.sqlUtil import getsql


def init():
    global logger
    global engine, path, date, data, mysql
    global lastOperateTimeSql, cur_path
    global growthSQl, marketSQl, industrySQL, industrySQL2, peSQL
    dirname, filename = os.path.split(os.path.abspath(__file__))
    # print(dirname)
    cur_path=dirname
    logger = logging.getLogger(__name__)
    logger.setLevel(level = logging.INFO)
    handler = logging.FileHandler(os.path.join(cur_path,"log.txt"))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    lastOperateTimeSql="select max(updateTime) from tb_operation_time where name='{}'"
    data=utils.loadData.loadData('config.yml')
    growthSQl=getStrSQL('growth')
    industrySQL=getStrSQL('industrySQL')
    industrySQL2=getStrSQL('industrySQL2')
    peSQL=getStrSQL('peSQL')
    date=datetime.datetime.now().date()
    engine=create_engine(data['db'])
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