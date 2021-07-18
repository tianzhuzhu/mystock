'阿里巴巴概念'
import pandas as pd

import configger
from data.akshare.industry_concept import query_concept_index

data=pd.DataFrame(index=[1,2,3,4],data={'a':[1,2,3,4]})
data2=pd.DataFrame(index=[1,2],data={'a':[1,2]})
# print(data)
# print(data2)
# print(not data['a'].isin(data2['a']))
# print(data['a'].isin(data2['a']))
# print(~data['a'].isin(data2['a']))