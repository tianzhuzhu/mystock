import datetime
import os

import database
import myEmail.send
import utils.util as util
import pandas as pd
from sqlalchemy import create_engine

import utils.loadData

def getResultFile(th=1000,growth=0.3,pe=20):
    database.init()
    path=database.path
    date=database.date
    data=findStockList(100,th,growth,pe)
    if(not os.path.exists(path)):
        os.mkdir(path)
    filepath=os.path.join(path,'市值{}市盈率{}增长率{}.xlsx'.format('500亿','25','25%'))
    data.to_excel(filepath)
    print(filepath)
    # myEmail.send.send_mail(filepath)
    return filepath
def findStockList(days=100,th=1000,growth=0.3,pe=20):

    data=util.findDataBymarkevalueTH(th)
    data= util.findGrowhBydata(data,growth)
    result= util.getRecentDataBydata(data)
    # print(result)
    result=util.fliterPeByData(result,pe)
    # print(result)
    result=util.findVolumeCountByData(result)
    return result

# ,'peTTM','pbMRQ'
#阈值单位亿



if __name__ == '__main__':
    result=findStockList()
    # print(result['YOYNI'])
    # result.to_excel('a.xlsx')
    # print(result)
##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



