from sqlalchemy import create_engine

import utils.loadData


def init():
    global engine,ad
    data=utils.loadData.loadData('config.yml')
    engine=create_engine(data['db'])