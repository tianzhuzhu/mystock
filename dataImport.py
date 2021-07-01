import sys
import threading

from data.akshare.industry_concept import save_data
from data.akshare.north_net_flow import save_north_data
from data.akshare.yjbb import update_allow_basic_information

if __name__ == '__main__':
    try:
        args1=sys.argv[1]
    except:
        args1='byhand'
    t1=threading.Thread(target=save_data,args=(100,args1))
    t2=threading.Thread(target=update_allow_basic_information,args=(args1,))
    t3=threading.Thread(target=save_north_data,args=('tb_ak_north_hold_stock','tb_ak_north_board_rank',args1))
    threads = [t1,t2,t3]
    for t in threads:
        t.setDaemon(False)
        t.start()

    # importToday()
    # importTodayStockAndPE()
    # # main.init()
    # # main.process5(main.data)
    # # main.process4(main.data)
    # # main.process6(main.data)
    # main.init()
    # getAllMarketValue()
    # tabledict={
    # 'tb_growth':queryGrowthByCode,
    # 'tb_profit':queryProfitByCode,
    # 'tb_stock_dupont':queryDubpontByCode,
    # 'tb_operation':queryOperationByCode,
    # 'tb_balance':queryBalanceByCode,
    # 'tb_cash_flow':queryCashFlowByCode,
    #  }
    #
    # #  'tb_performance_Express_Report':queryPerformanceExpressReportByCode,
    # # #  'tb_forecast_Report':queryForecastReport,
    # l=len(tabledict)
    # print(tabledict.keys())
    # for k,v in tabledict.items():
    #     importBasicData(k,v)
    #     time.sleep(60)
    # try:
    #     main.process5(main.data)
    #     main.process4(main.data)
    #     main.process6(main.data)
    # except:
    #     pass
    # tabledict={
    #     'tb_performance_express_report':queryPerformanceExpressReportByCode,
    #     'tb_forecast_report':queryForecastReport,
    # }
    # for k,v in tabledict.items():
    #     importReport(k,v)



