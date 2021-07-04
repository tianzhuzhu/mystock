import sys
import threading
import time

import utils
from data.akshare.industry_concept import save_data
from data.akshare.north_net_flow import save_north_data
from data.akshare.yjbb import update_allow_basic_information
from data.baostack.baseImport import queryGrowthByCode, queryProfitByCode, queryDubpontByCode, queryOperationByCode, \
    queryBalanceByCode, queryCashFlowByCode, importBasicData
from data.baostack.importReportData import queryPerformanceExpressReportByCode, queryForecastReport, importReport
from data.baostack.importStockAndPE import importTodayStockAndPE
from data.baostack.importTodayStock import importToday
from utils.util import getAllMarketValue


def importBasic(key):
    opertation='all_per_day_data'
    if( key=='byhand' or utils.timeUtil.tableNeedUpdate(opertation)):
        importToday()
        importTodayStockAndPE()
        getAllMarketValue()
        tabledict = {
            'tb_growth': queryGrowthByCode,
            'tb_profit': queryProfitByCode,
            'tb_stock_dupont': queryDubpontByCode,
            'tb_operation': queryOperationByCode,
            'tb_balance': queryBalanceByCode,
            'tb_cash_flow': queryCashFlowByCode,
        }
        for k, v in tabledict.items():
            importBasicData(k, v)
            time.sleep(60)
        tabledict = {
            'tb_performance_express_report': queryPerformanceExpressReportByCode,
            'tb_forecast_report': queryForecastReport,
        }
        for k, v in tabledict.items():
            importReport(k, v)
        utils.timeUtil.saveOperationTime(opertation)


if __name__ == '__main__':
    try:
        args1=sys.argv[1]
    except:
        args1='byhand'
        time.sleep(5)
        print('all start')
        threads = []
        # t1=threading.Thread(target=save_data,args=(100,args1))
        # threads.append(t1)
        t2=threading.Thread(target=update_allow_basic_information,args=(args1,))
        threads.append(t2)
        t3=threading.Thread(target=save_north_data,args=('tb_ak_north_hold_stock','tb_ak_north_board_rank',args1))
        threads.append(t3)
        t4=threading.Thread(target=importBasic,args=(args1))
        threads.append(t4)
        for t in threads:
            t.setDaemon(False)
            t.start()


    # try:
    #     .process5(main.data)
    #     main.process4(main.data)
    #     main.process6(main.data)
    # except:
    #     pass
    tabledict={
        'tb_performance_express_report':queryPerformanceExpressReportByCode,
        'tb_forecast_report':queryForecastReport,
    }
    for k,v in tabledict.items():
        importReport(k,v)



