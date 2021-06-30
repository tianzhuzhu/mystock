# #季度报
# date	str	Y	date="20200331"; choice of {"XXXX0331", "XXXX0630", "XXXX0930", "XXXX1231"}; 从 20081231 开始
import akshare as ak
stock_em_yjbb_df = ak.stock_em_yjbb(date="20200331")
print(stock_em_yjbb_df)


# #快报
# import akshare as ak
# stock_em_yjkb_df = ak.stock_em_yjkb(date="20200331")
# print(stock_em_yjkb_df)


# 业绩预告
# import akshare as ak
# stock_em_yjyg_df = ak.stock_em_yjyg(date="20190331")
# print(stock_em_yjyg_df)

#预披露时间
# import akshare as ak
# stock_em_yysj_df = ak.stock_em_yysj(date="20190331")
# print(stock_em_yysj_df)

#利润表

# import akshare as ak
# stock_em_lrb_df = ak.stock_em_lrb(date="20200331")
# print(stock_em_lrb_df)

# 现金流量表

# import akshare as ak
# stock_em_xjll_df = ak.stock_em_xjll(date="20200331")
# print(stock_em_xjll_df)

#资产负债表

import akshare as ak
stock_em_zcfz_df = ak.stock_em_zcfz(date="20200331")
print(stock_em_zcfz_df)
