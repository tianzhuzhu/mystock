import random
import time

from data.importBasicInformation import queryGrowthByCode, queryDubpontByCode, queryProfitByCode, queryOperationByCode, \
    queryBalanceByCode, queryCashFlowByCode, queryPerformanceExpressReportByCode, queryForecastReport, importBasicData

from data.importStockAndPE import importTodayStockAndPE
from data.importTodayStock import importToday
from utils.util import todayStock, getAllMarketValue

if __name__ == '__main__':

    importTodayStockAndPE()
    tabledict={
     'tb_growth':queryGrowthByCode,
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
        time.sleep(100)
    getAllMarketValue()
    importToday()


