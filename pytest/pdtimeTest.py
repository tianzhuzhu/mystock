import datetime

import pandas as pd

#  PeriodIndex(['2016Q1', '2016Q2', '2016Q3', '2016Q4', '2017Q1'], dtype='period[Q-MAR]', freq='Q-MAR')
quarters = pd.period_range('2016Q1', '2017Q1', freq='Q-MAR')
print(quarters)
quarters.asfreq('D', 'E')
print(quarters)



df=pd.DataFrame()
df.loc[0,'date']=datetime.datetime.now()
print(df)
df=df['date'].dt.to_period('Q')
# df=df['date'].dt.quarter

print(df)
start=pd.to_datetime('1991-9-1')
def get_this_end_quarter_day(z):
    x2 = z + pd.tseries.offsets.DateOffset(months=3 - ((z.month - 1) % 3), days=-z.day)  # 当季最后一天
    return x2
def get_last_end_quarter_day(z):
    x2 = z + pd.tseries.offsets.DateOffset(months=-((z.month - 1) % 3), days=-z.day)  # 当季最后一天
    return x2
z=pd.to_datetime('1991-1-1')
x1=get_last_end_quarter_day(z)
print(x1)
x2=get_this_end_quarter_day(z)
print(x2)
data=pd.period_range(start=start,end=x2,freq='q')
data=data.values.astype('datetime64[D]')
print(data)
# data=pd.DataFrame(data)
# print(data[0].values.astype('datetime64[D]'))
