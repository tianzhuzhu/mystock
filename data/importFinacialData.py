import akshare as ak
# stock_financial_abstract_df = ak.stock_financial_abstract(stock="600004")
# print(stock_financial_abstract_df.columns)
# print(stock_financial_abstract_df)
# stock_financial_analysis_indicator_df = ak.stock_financial_analysis_indicator(stock="600004")
# print(stock_financial_analysis_indicator_df)
stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="利润表")
print(stock_financial_report_sina_df)