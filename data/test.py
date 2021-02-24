import datetime
import random
import time

import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
import pymysql
if(pd.to_datetime('2021-2-23').date()==datetime.datetime.now().date()):
    print(1)

# BasicData = ak.stock_a_lg_indicator(stock=i)
# BasicData.sort_values('trade_date', inplace=True)
# maxDate = BasicData.iloc[0]
# print(maxDate)
# maxDate['code'] = i
# peData = data.append(maxDate, ignore_index=True)
# print('pedata')
# print(peData)
# peData.to_sql('pehistory', con=engine, if_exists='append')


