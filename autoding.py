import threading
import time

from data.akshare.industry_concept import save_data
from data.akshare.yjbb import update_allow_basic_information, update_forecast
from dataHandler.akshare.conpcet_index import get_industry_index
from utils.dingding_util import send_messsage_byexcel, send_recent_forecat_by_sql
from utils.timeUtil import *

def notice_concept(operation):
    print(operation)
    while(True):
        if(tableNeedUpdate(operation,days=1)==True and datetime.datetime.now().hour>7):
            save_data(way='byboot')
            print('start')
            data=get_industry_index()
            send_messsage_byexcel(data)
            saveOperationTime(operation)
        time.sleep(1800)
def send_recent_forecat(operation):
    while(True):
        if(tableNeedUpdate(operation,days=1)==True and datetime.datetime.now().hour>6):
            update_forecast(way='byboot')
            print('start')
            send_recent_forecat_by_sql()
            saveOperationTime(operation)
        time.sleep(1800)
if __name__=='__main__':
    operation1='dingding_notice'
    threads = []
    t1=threading.Thread(target=notice_concept,args=(operation1,))
    operation2='dingding_forecast_notice'
    t2=threading.Thread(target=send_recent_forecat,args=(operation2,))
    threads.append(t1)
    for t in threads:
        t.setDaemon(False)
        t.start()




