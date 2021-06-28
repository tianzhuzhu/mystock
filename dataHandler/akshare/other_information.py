# 涨停股池
# 接口: stock_em_zt_pool
#
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=ztgc
#
# 描述: 获取东方财富网-行情中心-涨停板行情-涨停股池
#
# 限量: 单次返回所有涨停股池数据
#
# 输入参数
#
# 名称	类型	必选	描述
# date	str	Y	date='20210525'
# 输出参数
#
# 名称	类型	默认显示	描述
# 序号	int32	Y	-
# 代码	object	Y	-
# 名称	object	Y	-
# 涨跌幅	float64	Y	注意单位: %
# 最新价	int64	Y	-
# 成交额	int64	Y	-
# 流通市值	float64	Y	-
# 总市值	float64	Y	-
# 换手率	float64	Y	注意单位: %
# 封板资金	int64	Y	-
# 首次封板时间	int64	Y	注意格式: 09:25:00
# 最后封板时间	int64	Y	注意格式: 09:25:00
# 炸板次数	int64	Y	-
# 涨停统计	object	Y	-
# 连板数	int64	Y	注意格式: 1 为首板
# 所属行业	object	Y	-
# 接口示例
import datetime

import akshare as ak
import pandas as pd


def zt_stock_list(date=datetime.datetime.now().date()):
    date=pd.to_datetime(str(date)).strftime('%Y%m%d')
    date=str(date)
    data = ak.stock_em_zt_pool(date=date)
    print(data)
    return data


