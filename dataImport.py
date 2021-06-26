import _thread
import random
import time

import main
from data.baseImport import queryGrowthByCode, queryDubpontByCode, queryProfitByCode, queryOperationByCode, \
    queryBalanceByCode, queryCashFlowByCode, importBasicData
from data.importReportData import queryPerformanceExpressReportByCode, queryForecastReport, importReport

from data.importStockAndPE import importTodayStockAndPE
from data.importTodayStock import importToday
from dataHandler.akshare.industry_concept import save_data
from dataHandler.akshare.yjbb import update_allow_basic_information
from utils.util import todayStock, getAllMarketValue
def save_industry_and_concept():
    save_data()

if __name__ == '__main__':

    _thread.start_new_thread(save_industry_and_concept, ())
    _thread.start_new_thread(update_allow_basic_information, ())

    importToday()
    importTodayStockAndPE()
    # main.init()
    # main.process5(main.data)
    # main.process4(main.data)
    # main.process6(main.data)
    main.init()
    getAllMarketValue()
    tabledict={
    'tb_growth':queryGrowthByCode,
    'tb_profit':queryProfitByCode,
    'tb_stock_dupont':queryDubpontByCode,
    'tb_operation':queryOperationByCode,
    'tb_balance':queryBalanceByCode,
    'tb_cash_flow':queryCashFlowByCode,
     }

    #  'tb_performance_Express_Report':queryPerformanceExpressReportByCode,
    # #  'tb_forecast_Report':queryForecastReport,
    l=len(tabledict)
    print(tabledict.keys())
    for k,v in tabledict.items():
        importBasicData(k,v)
        time.sleep(60)
    try:
        main.process5(main.data)
        main.process4(main.data)
        main.process6(main.data)
    except:
        pass
    tabledict={
        'tb_performance_express_report':queryPerformanceExpressReportByCode,
        'tb_forecast_report':queryForecastReport,
    }
    for k,v in tabledict.items():
        importReport(k,v)
    time.sleep(60)



