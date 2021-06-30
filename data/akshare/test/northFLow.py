import akshare as ak
# 沪股通 深股通 北上
# stock_em_hsgt_north_net_flow_in_df = ak.stock_em_hsgt_north_net_flow_in(indicator="沪股通")
# print(stock_em_hsgt_north_net_flow_in_df)
# # stock_em_hsgt_north_net_flow_in_df = ak.stock_em_hsgt_north_net_flow_in(indicator="深股通")
# # print(stock_em_hsgt_north_net_flow_in_df)
#
#
# # import akshare as ak
# #累计
# stock_em_hsgt_north_acc_flow_in_df = ak.stock_em_hsgt_north_acc_flow_in(indicator="沪股通")
# print(stock_em_hsgt_north_acc_flow_in_df)

#北向板块
# symbol	str	Y	symbol="北向资金增持行业板块排行"; choice of {"北向资金增持行业板块排行", "北向资金增持概念板块排行", "北向资金增持地域板块排行"}
# indicator	str	Y	indicator="今日"; choice of {"今日", "3日", "5日", "10日", "1月", "1季", "1年"}

# import akshare as ak
# stock_em_hsgt_industry_rank_df = ak.stock_em_hsgt_board_rank(symbol="北向资金增持行业板块排行", indicator="今日")
# print(stock_em_hsgt_industry_rank_df)

#个股排行

# market	str	Y	market="沪股通"; choice of {"北向", "沪股通", "深股通"}
# indicator	str	Y	indicator="沪股通"; choice of {"今日排行", "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"}

# import akshare as ak
# stock_em_hsgt_hold_stock_df = ak.stock_em_hsgt_hold_stock(market="北向", indicator="今日排行")
# print(stock_em_hsgt_hold_stock_df)

#每日个股统计
# 名称	类型	必选	描述
# symbol	str	Y	symbol="北向持股"; choice of {"北向持股", "沪股通持股", "深股通持股", "南向持股"}
# start_date	str	Y	start_date="20200713"; 此处指定近期交易日
# end_date	str	Y	end_date="20200714"; 此处指定近期交易日

# import akshare as ak
# stock_em_hsgt_stock_statistics_df = ak.stock_em_hsgt_stock_statistics(symbol="南向持股", start_date="20201218", end_date="20201218")
# print(stock_em_hsgt_stock_statistics_df)

# 每日机构统计

# stock_em_hsgt_institution_statistics_df = ak.stock_em_hsgt_institution_statistics(market="北向持股", start_date="20201218", end_date="20201218")
# print(stock_em_hsgt_institution_statistics_df)

# stock_em_hsgt_hist_df = ak.stock_em_hsgt_hist(symbol="港股通沪")
# print(stock_em_hsgt_hist_df)