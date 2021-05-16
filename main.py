import time
import traceback

import choose.byVolume as volume
import choose.bygrowthAndPe  as PE
import database
from choose.marketValuePeGrowh import getResultFile
from data import importStockAndPE as importStockAndPE
import utils.loadData
from data import importGrowth
from data import importTodayStock
import myEmail.send as send
import _thread
def init():
    global data
    data=utils.loadData.loadData('config.yml')
def process1(data):
    time.sleep(60)
    importTodayStock.importToday()
    print('process1 开始')
    list=[220]
    print(list)
    for i in list:
        result =volume.choose(i,1.2)
    results=[result]
    namelist=['根据成交量.xlsx']
    # send.send_mail(results,namelist,data)
def process2(data):

    print(data)
    importStockAndPE.importTodayStockAndPE()
    # importGrowth.importGrowth()
    pelist=[10,15,20,30]
    # pelist=[10]
    resultlist=[]
    namelist=[]
    for i in pelist:
        print('process2 开始')
        resultlist.append(PE.getStockList(i,0.6,120))
        namelist.append('pe{}-growth{}.xlsx'.format(i,0.6))

    send.send_mail(resultlist,namelist,data)
def process4(data):
    result=getResultFile()
    send.send_mail([result],['结果.xlsx'],data)
def process5(data):
    result=getResultFile(th=200,growth=0.2,pe=25,ByMACD=True)
    send.send_mail([result],['MACD结果.xlsx'],data)
def process6(data):
    result=getResultFile(th=200,growth=0.2,pe=25,ByMACD=False,BySMA=True)
    send.send_mail([result],['SMA结果.xlsx'],data)

if __name__ == '__main__':

    database.init()
    data=utils.loadData.loadData('config.yml')
    try:
        _thread.start_new_thread( process1, (data,) )
        # _thread.start_new_thread( process3, () )
    except:
        traceback.print_exc()
    process5(data)
    process4(data)
    process2(data)
    process4(data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
