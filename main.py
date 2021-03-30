import time
import traceback

import choose.byVolume as volume
import choose.bygrowthAndPe  as PE
from data import importStockAndPE as importStockAndPE
import utils.loadData
from data import importGrowth
from data import importTodayStock
import myemail.send as send
import _thread
def process1(data):
    time.sleep(60)
    # importTodayStock.importToday()
    print('process1 开始')
    list=[220]
    print(list)
    for i in list:
        result =volume.choose(i,1.2)
    results=[result]
    namelist=['根据成交量.xlsx']
    send.send_mail(results,namelist,data)
def process2(data):

    print(data)
    # importStockAndPE.importTodayStockAndPE()
    # importGrowth.importGrowth()
    pelist=[10,15,20,30]
    # pelist=[10]
    resultlist=[]
    namelist=[]
    for i in pelist:
        print('process2 开始')
        resultlist.append(PE.getStockList(i,0.6,90))
        namelist.append('pe{}-growth{}.xlsx'.format(i,0.6))

    send.send_mail(resultlist,namelist,data)
def process3():
    importGrowth.importGrowth()
if __name__ == '__main__':
    data=utils.loadData.loadData('config.yml')
    print(data)

    try:
        # _thread.start_new_thread( process1, (data,) )
        _thread.start_new_thread( process2, (data,) )
        # _thread.start_new_thread( process3, () )
    except:
        traceback.print_exc()

    time.sleep(7200)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
