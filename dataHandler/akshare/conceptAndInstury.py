import akshare as ak
# 获取行业各个股票
df=ak.stock_board_industry_name_ths()
for i in df['name']:
    print(i)
    #成分股
    stock_board_industry_cons_ths_df = ak.stock_board_industry_cons_ths(symbol=i)
    #指数
    stock_board_industry_index_ths_df = ak.stock_board_industry_index_ths(symbol="半导体及元件")
    print(stock_board_industry_cons_ths_df)
#
# 获取所有概念
df=ak.stock_board_concept_name_ths()
print(df)
for i in df['name']:
    print(i)
    #成分股
    stock_board_concept_cons_ths_df = ak.stock_board_concept_cons_ths(symbol=i)
    print(stock_board_concept_cons_ths_df)
    #指数
    stock_board_concept_index_ths_df = ak.stock_board_concept_index_ths(symbol=i)