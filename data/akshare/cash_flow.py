# 板块资金流排名
# 接口: stock_sector_fund_flow_rank
#
# 目标地址: http://data.eastmoney.com/bkzj/hy.html
#
# 描述: 获取东方财富网-数据中心-资金流向-板块资金流-排名
#
# 限量: 单次获取指定板块的指定期限的资金流排名数据
#
# 输入参数
#
# 名称	类型	必选	描述
# indicator	str	Y	indicator="5日"; choice of {"今日", "5日", "10日"}
# sector_type	str	Y	sector_type="地域资金流"; choice of {"行业资金流": "2", "概念资金流": "3", "地域资金流": "1"}
# 输出参数-行业资金流-今日
#
# 名称	类型	默认显示	描述
# 名称	str	Y	-
# 今日涨跌幅	str	Y	注意单位: %
# 主力净流入-净额	float	Y	-
# 主力净流入-净占比	float	Y	注意单位: %
# 超大单净流入-净额	float	Y	-
# 超大单净流入-净占比	float	Y	注意单位: %
# 大单净流入-净额	float	Y	-
# 大单净流入-净占比	float	Y	注意单位: %
# 中单净流入-净额	float	Y	-
# 中单净流入-净占比	float	Y	注意单位: %
# 小单净流入-净额	float	Y	-
# 小单净流入-净占比	float	Y	注意单位: %
# 主力净流入最大股	float	Y	-
# 接口示例-行业资金流-今日

import akshare as ak
stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator="10日", sector_type="行业资金流")
print(stock_sector_fund_flow_rank_df)
stock_sector_fund_flow_rank_df.to_excel('行业资金流.xlsx')

stock_sector_fund_flow_rank_df = ak.stock_sector_fund_flow_rank(indicator="10日", sector_type="概念资金流")
stock_sector_fund_flow_rank_df.to_excel('概念资金流.xlsx')
