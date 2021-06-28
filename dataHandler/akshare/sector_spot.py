# 板块行情
# 接口: stock_sector_spot
#
# 目标地址: http://finance.sina.com.cn/stock/sl/
#
# 描述: 获取新浪行业-板块行情
#
# 限量: 单次获取指定的板块行情实时数据
#
# 输入参数
#
# 名称	类型	必选	描述
# indicator	str	Y	indicator="新浪行业"; choice of {"新浪行业", "启明星行业", "概念", "地域", "行业"}
# 输出参数
#
# 名称	类型	默认显示	描述
# label	str	Y	-
# 板块	str	Y	-
# 公司家数	float	Y	-
# 平均价格	float	Y	-
# 涨跌额	float	Y	-
# 涨跌幅	float	Y	注意单位: %
# 总成交量(手)	float	Y	-
# 总成交额(万元)	float	Y	-
# 股票代码	str	Y	-
# 涨跌幅	float	Y	注意单位: %
# 当前价	float	Y	-
# 涨跌额	float	Y	-
# 股票名称	str	Y	-
import datetime
import random
import time

import akshare as ak

import database
from dataHandler.akshare.industry_concept import retry


def query_sector_list(indicator="新浪行业"):
    data = ak.stock_sector_spot(indicator=indicator)
    print(data)
    return data

# 板块详情
# 接口: stock_sector_detail
#
# 目标地址: http://finance.sina.com.cn/stock/sl/#area_1
#
# 描述: 获取新浪行业-板块行情-成份详情, 由于新浪网页提供的统计数据有误, 部分行业数量大于统计数
#
# 限量: 单次获取指定的新浪行业-板块行情-成份详情
#
# 输入参数
#
# 名称	类型	必选	描述
# sector	str	Y	sector="hangye_ZL01"; 通过 stock_sector_spot 返回数据的 label 字段选择 sector

# 接口示例
# @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000,wrap_exception=False,stop_max_attempt_number=10)
def query_secotr_detail(sector="hangye_ZL01"):
    data = ak.stock_sector_detail(sector=sector)
    print(data)
    return data

def save_secotr_Data(sector_list_table='tb_ak_sector_spot',sector_detail_table='tb_ak_sector_detail'):
    database.init()
    engine=database.engine
    sector_type_list=["新浪行业", "启明星行业", "概念", "地域", "行业"]
    for type in sector_type_list:
        time.sleep(random.randint(5))
        sector_list=query_sector_list(indicator=type)
        sector_list['update_time']=datetime.datetime.now().date()
        sector_list.to_sql(sector_list_table,con=engine,if_exists='append',index=False)
        for secotr in sector_list['label']:
            try:
                time.sleep(random.randint(3))
                data=query_secotr_detail(secotr)
                data['update_time'] = datetime.datetime.now().date()
                data['label']=secotr
                data['type']=type
                print(data)
                data.to_sql(sector_detail_table,con=engine,if_exists='append',index=False)
            except:
                print(type+" "+secotr+"error")
if __name__=='__main__':
    save_secotr_Data()
