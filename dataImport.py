import random
import time

import main
from data.importBasicInformation import queryGrowthByCode, queryDubpontByCode, queryProfitByCode, queryOperationByCode, \
    queryBalanceByCode, queryCashFlowByCode, importBasicData
from data.importReportData import queryPerformanceExpressReportByCode, queryForecastReport, importReport

from data.importStockAndPE import importTodayStockAndPE
from data.importTodayStock import importToday
from utils.util import todayStock, getAllMarketValue

if __name__ == '__main__':

    importToday()


    importTodayStockAndPE()
    main.init()
    main.process5(main.data)
    main.process4(main.data)
    main.process6(main.data)

    tabledict={
            'tb_performance_Express_Report':queryPerformanceExpressReportByCode,
            'tb_forecast_Report':queryForecastReport,
        }
    for k,v in tabledict.items():
        importReport(k,v)
    time.sleep(60)

    main.init()
    try:
        main.process5(main.data)
        main.process4(main.data)
        main.process6(main.data)
    except:
        pass

    tabledict={
     'tb_growth':queryGrowthByCode,
     'tb_profit':queryProfitByCode,
     'tb_stock_dupont':queryDubpontByCode,
    'tb_operation':queryOperationByCode,
    'tb_balance':queryBalanceByCode,
    'tb_cash_Flow':queryCashFlowByCode,
     }
    #  'tb_performance_Express_Report':queryPerformanceExpressReportByCode,
    # #  'tb_forecast_Report':queryForecastReport,
    l=len(tabledict)
    print(tabledict.keys())
    for k,v in tabledict.items():
        importBasicData(k,v)
        time.sleep(60)
    getAllMarketValue()




