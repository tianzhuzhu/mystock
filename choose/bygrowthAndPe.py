def getGrowth(code):
    sql='select code,max(date) from tb_stock_hisotry_detatil group by code'
def getStockList():
    sql=''
if __name__ == '__main__':
    pass

##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



