import datetime

from sqlalchemy import create_engine

import utils.loadData


def init():

    global engine,path,date,data
    global lastOperateTimeSql
    lastOperateTimeSql="select max(updateTime) from tb_operation_time where name='{}'"
    data=utils.loadData.loadData('config.yml')
    date=datetime.datetime.now().date()
    engine=create_engine(data['db'])
    path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\{}'.format(date)
