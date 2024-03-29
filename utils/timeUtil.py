import datetime
import pandas as pd

import configger
def get_this_end_quarter_day(date)->datetime.datetime:
    date = date + pd.tseries.offsets.DateOffset(months=3 - ((date.month - 1) % 3), days=-date.day)  # 当季最后一天
    return date
def get_last_end_quarter_day(date) ->datetime.datetime:
    date = date + pd.tseries.offsets.DateOffset(months=-((date.month - 1) % 3), days=-date.day)  # 当季最后一天
    return date


def get_no_chaging_date(date):
    date=pd.to_datetime(str(date)).strftime('%Y%m%d')
    date=str(date)
    return date
def get_chaging_date(date):
    date=pd.to_datetime(str(date)).strftime('%Y-%m-%d')
    date=str(date)
    return date


def saveOperationTime(name):
    configger.init()
    con=configger.engine
    operation=pd.DataFrame()
    operation.loc[0,'name']=name
    operation.loc[0,'updateTime']=datetime.datetime.now()
    operation.to_sql(name='tb_operation_time',con=con,if_exists='append',index=False)
    return True
def tableNeedUpdate(tableName,days=1,isWorkDay=True):
    configger.init()
    # 显示登陆返回信息
    # 结果集输出到csv文件
    con=configger.engine
    try:
        sql=configger.lastOperateTimeSql.format(tableName)
        lastTime=pd.read_sql(sql=sql,con=con).iloc[0,0]
        now=datetime.datetime.now()
        print(lastTime)
    except:
        return True
    if(lastTime==None):
        return True
    if(days==1):
        if(needUpdate(lastTime,now,isWorkDay=isWorkDay)==False):
            return False
        return needUpdate(lastTime,now,isWorkDay=isWorkDay)
    else:
        return (pd.to_datetime(now.date())-pd.to_datetime(lastTime)).days>days




def needUpdate(lastUpdateTime,nowtime,isWorkDay=False):
    print(lastUpdateTime)
    print(nowtime)
    if(nowtime.hour<15):
        nowtime= nowtime - datetime.timedelta(days=1)
    if(lastUpdateTime.hour<15):
        lastUpdateTime= lastUpdateTime - datetime.timedelta(days=1)
    days=(nowtime.date()-lastUpdateTime.date()).days
    if(isWorkDay==True):
        #3天必更
        if(days>=3):
            return True
        if(days==2):
            if(nowtime.weekday()==6):
                return False
            else: return True
        if(days==1):
            if(nowtime.weekday()==6 or nowtime.weekday()==5):
                return False
            else: return True
        return False

    else:
        #非工作日判断
        #隔了2天
        if(days>=1):
            return True
        else:
            return False

def data_need_update(tablename,time,keyname,key) ->bool:
    configger.init()
    engine=configger.engine
    try:
        sql='select max({}) from {} where {}="{}"'.format(time,tablename,keyname,key)
        date=pd.read_sql(sql=sql,con=engine).iloc[0,0]
        now=datetime.datetime.now().date()
        date=pd.to_datetime(date).date()
        if(now-date).days>0:
            return True
        else:
            return False
    except:
        return True