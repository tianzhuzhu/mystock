import pandas as pd
def deleteNullColumn(data,column):
    data[column]=data[column].map(lambda x:x.strip())
    data.dropna(subset=[],inplace=True)
    data=data.loc[data[column]!='']
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