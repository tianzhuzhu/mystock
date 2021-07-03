import pandas as pd

import configger


def select_growth_data(code=''):
    configger.init()
    engine=configger.engine
    sql=configger.all_growthSQL
    if(code==''):
        data=pd.read_sql(sql=sql,con=engine)
    print(data)

print(select_growth_data())