import random

from data.importBasicInformation import queryGrowthByCode, queryDubpontByCode, queryProfitByCode, queryOperationByCode, \
    queryBalanceByCode, queryCashFlowByCode, queryPerformanceExpressReportByCode, queryForecastReport, importBasicData
from data.importGrowth import importGrowth
from data.importProfit import importProfit
from data.importStockAndPE import importTodayStockAndPE
from utils.util import todayStock, getAllMarketValue

if __name__ == '__main__':
    # importTodayStockAndPE()

    list=[importProfit,importGrowth]
    tabledict={'tb_growth':queryGrowthByCode,

     'tb_profit':queryProfitByCode,
     'tb_stock_dupont':queryDubpontByCode,
     'tb_operation':queryOperationByCode,
     'tb_balance':queryBalanceByCode,
     'tb_cashFlow':queryCashFlowByCode,
     'tb_performanceExpressReport':queryPerformanceExpressReportByCode,
     'tb_forecastReport':queryForecastReport,
     }
    l=len(tabledict)
    print(tabledict.keys())
    for k,v in tabledict.items():
        importBasicData(k,v)


    # getAllMarketValue()


