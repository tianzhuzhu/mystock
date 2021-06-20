import akshare as ak
stock_em_dxsyl_df = ak.stock_em_dxsyl(market="上海主板")
print(stock_em_dxsyl_df)
stock_em_dxsyl_df.to_excel('a.xlsx')