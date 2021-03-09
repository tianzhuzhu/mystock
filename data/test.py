import akshare as ak
# # stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="现金流量表")
# stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="资产负债表")
stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600519", symbol="利润表")
stock_financial_report_sina_df.to_excel('a.xlsx')


import baostock as bs
import pandas as pd
year_list=range(2021)
print(year_list)

#### 登陆系统 ####
import baostock as bs
import pandas as pd

# 登陆系统
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

# 成长能力
growth_list = []
rs_growth = bs.query_growth_data(code="sh.600000", year=2017, quarter=2)
while (rs_growth.error_code == '0') & rs_growth.next():
    growth_list.append(rs_growth.get_row_data())
result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)
# 打印输出
print(result_growth)
# 结果集输出到csv文件
result_growth.to_csv("D:\\growth_data.csv", encoding="gbk", index=False)

# 登出系统
bs.logout()

stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="600004", symbol="现金流量表")
print(stock_financial_report_sina_df)

