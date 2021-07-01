import baostock as bs
import pandas as pd

import configger
from utils import timeUtil
from utils.timeUtil import tableNeedUpdate, saveOperationTime


def UpdateIndustryData(code='',date=''):
# 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    # 获取行业分类数据
    rs = bs.query_stock_industry(code,date)
    # rs = bs.query_stock_basic(code_name="浦发银行")
    needUpdate=tableNeedUpdate('tb_industry_information')
    print(needUpdate)
    if(needUpdate==True):
    # 打印结果集
        industry_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录，将记录合并在一起
            industry_list.append(rs.get_row_data())
        result = pd.DataFrame(industry_list, columns=rs.fields)
        # 结果集输出到csv文件
        # result.to_csv("D:/stock_industry.csv", encoding="gbk", index=False)
        result.rename(columns={'code_name':'名称','industry':'行业','industryClassification':'所属行业类别'},inplace=True)
        # 登出系统
        bs.logout()
    
        print(result)
        try:
            result.to_sql(name='tb_industry_information', con=configger.engine, if_exists='append', index=False)
            saveOperationTime('tb_industry_information')
        except:
            print('industry 更新失败')
        return result
    return pd.DataFrame()