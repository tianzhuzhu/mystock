import datetime

from sqlalchemy import create_engine

import utils.loadData


def init():

    global engine,path,date,data
    data=utils.loadData.loadData('config.yml')
    date=datetime.datetime.now().date()
    engine=create_engine(data['db'])
    path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\{}'.format(date)
