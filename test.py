from datetime import datetime
import pandas as pd
operation=pd.DataFrame()
operation.loc[0,'name']='tb_today_industry'
operation.loc[0,'updateTime']=datetime.now().date()
print(operation)