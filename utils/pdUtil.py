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
#'600000'->'sh.600000'
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