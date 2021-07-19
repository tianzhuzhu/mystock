import pandas as pd
def removeUnameColumns(data):
    data.dropna(inplace=True,how='all')
    columns=data.columns.tolist()
    for i in columns:
        if(i.startswith('Unnamed')):
            columns.remove(i)
    return pd.DataFrame(data,columns=columns)
def save_excel(path,dict:dict):
    i=0
    for k,v in dict.items():
        if (i == 0):
            v.to_excel(path, sheet_name=k)
            i=i+1
        else:
            with pd.ExcelWriter(path, mode='a') as writer:
                v.to_excel(writer, sheet_name=k)
    return path