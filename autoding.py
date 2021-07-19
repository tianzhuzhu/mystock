import time

from data.akshare.industry_concept import save_data
from dataHandler.akshare.industry_index import get_industry_index
from utils.dingding_util import send_messsage_byexcel
from utils.timeUtil import *

if __name__=='__main__':
    operation='dingding_notice'
    while(True):
        if(tableNeedUpdate(operation,days=1)==True and datetime.datetime.now().hour>8):
            #保存概念行业数据
            save_data(way='byboot')
            print('start')
            data=get_industry_index()
            send_messsage_byexcel(data)
            data = get_industry_index(key='概念')
            send_messsage_byexcel(data)
            saveOperationTime(operation)
        time.sleep(1800)