import datetime
import os

from sqlalchemy import create_engine
import logging
import utils.loadData
from utils import PC_util
from utils.sqlUtil import getsql
def getStrSQL(sql):
    sql=data['sql'][sql]
    sql=os.path.join(cur_path,sql)
    sql=getsql(sql)
    return sql
dirname, filename = os.path.split(os.path.abspath(__file__))
cur_path=dirname
lastOperateTimeSql="select max(updateTime) from tb_operation_time where name='{}'"
data=utils.loadData.loadData('config.yml')
growthSQl=getStrSQL('growth')
industrySQL=getStrSQL('industrySQL')
industrySQL2=getStrSQL('industrySQL2')
peSQL=getStrSQL('peSQL')
all_growthSQL=getStrSQL('akshare_all_growth')
date=datetime.datetime.now().date()
constant_variables=data['constant_variables']
path=r'选股\KLine\{}'.format(date)
save_place=os.path.join(dirname,r'选股\data\{}'.format(data))
T=2
if(PC_util.getname().find('G15')>0):
    db=data['db']['local_g15']
else:
    db = data['db']['g15']
def init():
    global engine, mysql
    global db
    try:
        engine=create_engine(db)
        mysql=engine
    except:
        db = data['db']['locahost']
        engine = create_engine(db)
        mysql = engine
    # print(db)


list=[]
def getEngine():
    global db
    global list
    if(len(list)==0):
        try:
            engine = create_engine(db)
        except:
            db = data['db']['locahost']
            engine = create_engine(db)
    else:
        engine=list.pop()
    return engine
def colseEngine(engine):
    global list
    list.append(engine)
if __name__=='__main__':
    init()