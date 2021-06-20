import akshare as ak
# 获取行业各个股票
df=ak.stock_board_industry_name_ths()
for i in df['name']:
    print(i)
    stock_board_industry_cons_ths_df = ak.stock_board_industry_cons_ths(symbol=i)
    print(stock_board_industry_cons_ths_df)
#
# 获取所有概念
df=ak.stock_board_concept_name_ths()
print(df)
for i in df['name']:
    print(i)
    stock_board_concept_cons_ths_df = ak.stock_board_concept_cons_ths(symbol=i)
    print(stock_board_concept_cons_ths_df)