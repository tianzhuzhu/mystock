import datetime
import os
import myEmail.send
import utils.util as util
import pandas as pd
from sqlalchemy import create_engine

import utils.loadData


def search(x,n):
    # print(x.columns)
    x=x[0:n]
    todayvolume=x.loc[x['date'].max()==x['date'],'volume'].iloc[0]
    print(todayvolume)
    x['close']=  x['close'].apply(float)
    avg=x['close'].mean()

    sumv=(x['volume']>todayvolume).apply(int).sum()
    data=x.loc[x['date']==x['date'].max(),['YOYNI','peTTM','pbMRQ','close']]
    data=data.iloc[0]
    # return pd.Series({'sum':sumv,'增长率':data.iloc[0,0],'pe':data.iloc[0,1],'pb':data.iloc[0,2]})
    data['count']=sumv
    data['avg']=data['close']/avg

    return data
# ,'peTTM','pbMRQ'

def getStockList( k=20,growth=0.5,days=90):
    data=utils.loadData.loadData('config.yml')
    sqlpath=data['sql']['peGrowth']
    sqlpath=os.path.join(os.path.abspath(os.path.dirname(__file__)),sqlpath)
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/stock')
    sqlTemplate=util.getsql(sqlpath)
    sql=sqlTemplate.format(k,growth)
    data=pd.read_sql(sql=sql,con=engine)
    print(data)
    data=data.groupby('code').apply(lambda x:search(x,days))
    data.sort_values(by='YOYNI',inplace=True,ascending=False)
    data=data[0:20]
    data.sort_values(by='peTTM',inplace=True,ascending=False)
    data=data[0:15]
    data.sort_values(by='count',inplace=True,ascending=False)
    date=datetime.datetime.now().date()
    path=r'D:\onedrive\OneDrive - ncist.edu.cn\选股\{}'.format(date)
    if(not os.path.exists(path)):
        os.mkdir(path)
    filepath=os.path.join(path,'结果{}-{}.xlsx'.format(str(k),str(growth)))
    data=data[0:10]
    data.to_excel(filepath)
    # myEmail.send.send_mail(filepath)
    return filepath
def searchByLongPE():
    sql="select code,count(1) from tb_history_stock groupby code where ppNNi>0.3 and date>='2018-1-1'"
    pass
if __name__ == '__main__':
    getStockList()

##根据pe 和 增长 找到优质股票
##在优质股票中，挑选低估股票
##其具体表现为股价 低于均值，成交量下降



