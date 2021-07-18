import akshare as ak
import datetime

import pandas as pd

import configger
from logger.my_logger import logit
from utils.pdUtil import add_date_to_df, add_dot_to_code, a_dot_to_code


#返回沪深两市所有指数
from utils.timeUtil import data_need_update


@add_date_to_df()
def query_all_index_spot() ->pd.DataFrame:
    stock_zh_index_spot_df = ak.stock_zh_index_spot()
    stock_zh_index_spot_df.rename(columns={'代码':'code'},inplace=True)
    return stock_zh_index_spot_df
@add_date_to_df()
@add_dot_to_code()
def query_his_index_by_code(code='sz399812') ->pd.DataFrame:
    stock_zh_index_daily_em_df = ak.stock_zh_index_daily_em(symbol=code)
    stock_zh_index_daily_em_df['code']=code
    stock_zh_index_daily_em_df.rename(columns={'代码': 'code'}, inplace=True)
    return stock_zh_index_daily_em_df

# data=query_all_index_spot()
@add_date_to_df()
@add_dot_to_code()
def query_index_content(code='sh000001'):
    code=code[2:]
    print(code)
    index_stock_cons_df = ak.index_stock_cons(index=code)
    index_stock_cons_df.rename(columns={'品种代码': 'code'}, inplace=True)
    return index_stock_cons_df
@logit()
def save_index_data(index_table='tb_ak_index_names',index_content='tb_ak_index_content',index_his='tb_ak_his_data'):
    configger.init()
    engine=configger.getEngine()
    all_index=query_all_index_spot()
    all_index_clone=a_dot_to_code(all_index.copy(),'code')
    datalist=[i for i in all_index['code']]
    content_df=pd.DataFrame()
    all_index_clone.to_sql(index_table,con=engine,if_exists='replace')
    for i in datalist:
        try:
            c = query_index_content(i)
            print(c)
        except:
            continue
        if(content_df.empty):
            content_df=c
        else:
            content_df=content_df.append(c)
    content_df.to_sql(index_content,con=engine,if_exists='replace')
    his_df = pd.DataFrame()
    for i in datalist:
        try:
            his=query_his_index_by_code(i)
            print(his)
        except:
            continue
        if (his_df.empty):
            his_df = his
        else:
            his_df = his_df.append(his)
    his_df.to_sql(index_content, con=engine, if_exists='replace')
    configger.colseEngine(engine)

save_index_data()
