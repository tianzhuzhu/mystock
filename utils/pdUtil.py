import datetime
from functools import update_wrapper, wraps

import numpy as np
import pandas as pd



def deleteNullColumn(data,column):
    data[column]=data[column].map(lambda x:str(x).strip())
    data.dropna(subset=[],inplace=True)
    data=data.loc[data[column]!='']
    data=data.loc[data[column]!='None']
    return data
def deleteNullColumns(data,columns):
    for column in columns:
        data[column]=data[column].map(lambda x:x.strip())
        data.dropna(subset=[],inplace=True)
        data=data.loc[data['column']!='']
    return data
def fillNullColumn(data,column,value):
    data[column]=data[column].map(lambda x:x.strip())
    data[column].fillna(value,inplace=True)
    data.loc[data[column]=='']=value
    return data
def fillNullColumns(data,columns,value):
    for column in columns:
        data[column]=data[column].map(lambda x:x.strip())
        data[column].fillna(value,inplace=True)
        data.loc[data[column]=='']=value
    return data
#'600000'->'sh.600000'
def attrs(**kwds):
    def decorate(f):
        for k in kwds:
            setattr(f, k, kwds[k])
        return f

    return decorate
def number_to_code(column='code'):
    def to_code(f):
        @wraps(f)
        def decorate(*args,**kwargs):
            res=f(*args,**kwargs)
            try:
                res=get_code_by_number(res,column)
            except:
                pass
            return res
        return decorate
    return to_code

def code_to_number(column='code'):
    def to_number(f):
        @wraps(f)
        def decorate(*args,**kwargs):
            res=f(*args,**kwargs)
            res=get_number_by_code(res,column)
            return res
        return decorate
    return to_number

def rename_index_to_code(column='代码'):
    def to_number(f):
        @wraps(f)
        def decorate(*args,**kwargs):
            res=f(*args,**kwargs)
            res.rename(column={column:'code'})
            return res
        return decorate
    return to_number


def get_code_by_number(data,column):
    def apply_number_to_code(x):
        x=str(x)
        if(x.startswith('6')):
            x='sh.'+x
        elif(x.startswith('3') or x.startswith('0')):
            x='sz.'+x
        return x
    data[column]=data[column].apply(lambda x:apply_number_to_code(x))
    return data
def get_number_by_code(data,column):
    def apply_number_to_code(x):
        x=str(x)
        if(x.startswith('sh.')):
            x=x[3:]
        elif(x.startswith('sz.')):
            x=x[3:]
        return x
    data[column]=data[column].apply(lambda x:apply_number_to_code(x))
    return data


def add_date_to_df(stf='%Y-%m-%d'):
    def add_date(f):
        @wraps(f)
        def decorate(*args,**kwargs):
            res=f(*args,**kwargs)
            date=datetime.datetime.now().date()
            date=date.strftime(stf)
            res['date']=date
            return res
        return decorate
    return add_date



#获取前多少条数据
def getRecnetN(x,n=8,column='date',ascending=False):
    x.reset_index(inplace=True)
    x.sort_values(by=[column],ascending=ascending,inplace=True)
    x=x[0:n]
    try:
        x.drop(columns=['index'],inplace=True)
        x.drop(columns=['code'],inplace=True)
    except:
        pass
    return x





@number_to_code(column='code')
def ab(data,*args,**kwargs):
    return data
@code_to_number()
def cd(data,*args,**kwargs):
    return data


if __name__=='__main__':

    a=pd.DataFrame(index=np.arange(10),data={'code':np.arange(10),'0':np.arange(10)})
    print(a.index.name,a.columns.names)
    print(a)
    a=ab(a)
    print(a)
    a=cd(a)
    print(a)

