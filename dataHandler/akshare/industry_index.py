import pandas as pd
from matplotlib import pyplot as plt

import configger

#key =行业/概念
from logger.my_logger import logit


@logit()
def get_industry_index(nlist=[3,7,14,31,100],key='行业')->pd.DataFrame:

    def find_growth_index(x:pd.DataFrame,nlist=nlist):
        x=x.copy()
        x.sort_values(by='日期',ascending=False)
        x=x[0:2*max(nlist)].copy()
        x.reset_index(inplace=True)
        res=pd.DataFrame()
        for n in nlist:
            str1=str(n)+'日涨跌幅'
            res.loc[0,str1]=((x.loc[0,'收盘价'])-(x.loc[n,'收盘价']))/x.loc[n,'收盘价']
            xc = x.shift(n)
            str2 = str(2*max(nlist))+'日内'+str(n) + '日最大涨跌幅'
            str3 = str(2*max(nlist))+'日内'+str(n) + '日最小涨跌幅'
            up_down=((xc['收盘价']-x['收盘价'])/x['收盘价'])[n:]
            print(up_down)
            print(max((up_down)),min(up_down))
            res.loc[0, [str2,str3]]=[max((up_down)),min(up_down)]
            # res.loc[0,str2],res.loc[0,str3]= \
            #     max((up_down)), min(up_down)
        return res
    sql='select * from tb_ak_industry_index' if key=='行业' else 'select * from tb_ak_concept_index'
    engine=configger.getEngine()
    data=pd.read_sql(con=engine,sql=sql)
    result=data.groupby(key).apply(lambda x:find_growth_index(x))
    result.index.names=[key,'序号']
    result.reset_index(level=1,drop=True,inplace=True)
    return result
get_industry_index()