import data.util as util
import pandas as pd
from sqlalchemy import create_engine


def search(x,n):
    x=x[0:n]
    todayvolume=x['date'].max()

    sumv=(x['volume']<todayvolume).apply(int).sum()
    ser=pd.Series({'code':x['code'],'count':sumv})
    return sumv

def getStockList():
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    sqlTemplate=util.getsql('peGrowth.sql')
    sql=sqlTemplate.format('0.5',15)
    data=pd.read_sql(sql=sql,con=engine)
    ser=data.groupby('code').apply(lambda x:search(x,220))
    ser.to_excel('a.xlsx')
        


if __name__ == '__main__':
    getStockList()

##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



