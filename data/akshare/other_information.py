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

import utils.timeUtil

#涨停股票
def query_zt_stock_list(date=datetime.datetime.now().date()):
    date=utils.timeUtil.get_no_chaging_date(date)
    data = ak.stock_em_zt_pool(date=date)
    date=datetime.datetime.now().date()
    data['date']=date
    return data

# 强势股池
# 接口: stock_em_zt_pool_strong
#
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=qsgc
#
# 描述: 获取东方财富网-行情中心-涨停板行情-强势股池
#
# 限量: 单次返回所有昨日涨停股池数据
#
# 输入参数
#
# 名称	类型	必选	描述
# date	str	Y	date='20210521'
# 输出参数
#
# 名称	类型	默认显示	描述
# 序号	int32	Y	-
# 代码	object	Y	-
# 名称	object	Y	-
# 涨跌幅	float64	Y	注意单位: %
# 最新价	float64	Y	-
# 涨停价	float64	Y	-
# 成交额	int64	Y	-
# 流通市值	float64	Y	-
# 总市值	float64	Y	-
# 换手率	float64	Y	注意单位: %
# 涨速	float64	Y	注意单位: %
# 是否新高	int64	Y	-
# 量比	float64	Y	-
# 涨停统计	object	Y	-
# 入选理由	object	Y	{'1': '60日新高', '2': '近期多次涨停', '3': '60日新高且近期多次涨停'}
# 所属行业	object	Y	-
# 接口示例

def query_strong_stock_pool(date=datetime.datetime.now().date()):
    date=utils.timeUtil.get_no_chaging_date(date)
    data = ak.stock_em_zt_pool_strong(date=date)
    date=datetime.datetime.now().date()
    data['date']=date
    return data

# 次新股池
# 接口: stock_em_zt_pool_sub_new
#
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=cxgc
#
# 描述: 获取东方财富网-行情中心-涨停板行情-次新股池
#
# 限量: 单次返回所有次新股池数据
#
# 输入参数
#
# 名称	类型	必选	描述
# date	str	Y	date='20210521'
# 输出参数
#
# 名称	类型	默认显示	描述
# 序号	int32	Y	-
# 代码	object	Y	-
# 名称	object	Y	-
# 涨跌幅	float64	Y	注意单位: %
# 最新价	float64	Y	-
# 涨停价	float64	Y	-
# 成交额	int64	Y	-
# 流通市值	float64	Y	-
# 总市值	float64	Y	-
# 转手率	float64	Y	注意单位: %
# 开板几日	int64	Y	-
# 开板日期	int64	Y	-
# 上市日期	int64	Y	-
# 是否新高	int64	Y	-
# 涨停统计	object	Y	-
# 所属行业	object	Y	-
# 接口示例

def query_sub_new_pool(date=datetime.datetime.now().date()):
    date=utils.timeUtil.get_no_chaging_date(date)
    data = ak.stock_em_zt_pool_sub_new(date=date)
    date=datetime.datetime.now().date()
    data['date']=date
    return data


# 炸板股池
# 接口: stock_em_zt_pool_zbgc
#
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=zbgc
#
# 描述: 获取东方财富网-行情中心-涨停板行情-炸板股池
#
# 限量: 单次返回所有炸板股池数据
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
# 最新价	float64	Y	-
# 涨停价	float64	Y	-
# 成交额	int64	Y	-
# 流通市值	float64	Y	-
# 总市值	float64	Y	-
# 换手率	float64	Y	注意单位: %
# 涨速	int64	Y	-
# 首次封板时间	object	Y	注意格式: 09:25:00
# 炸板次数	int64	Y	-
# 涨停统计	int64	Y	-
# 振幅	object	Y	-
# 所属行业	object	Y	-
# 接口示例

def query_zb_stock_pool(date=datetime.datetime.now().date()):
    date=utils.timeUtil.get_no_chaging_date(date)
    data = ak.stock_em_zt_pool_zbgc(date=date)
    date=datetime.datetime.now().date()
    data['date']=date
    print(data)
    return data

# 跌停股池
# 接口: stock_em_zt_pool_dtgc
#
# 目标地址: http://quote.eastmoney.com/ztb/detail#type=zbgc
#
# 描述: 获取东方财富网-行情中心-涨停板行情-跌停股池
#
# 限量: 单次返回所有跌停股池数据
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
# 最新价	float64	Y	-
# 成交额	int64	Y	-
# 流通市值	float64	Y	-
# 总市值	float64	Y	-
# 动态市盈率	float64	Y	-
# 换手率	float64	Y	注意单位: %
# 封单资金	int64	Y	-
# 最后封板时间	object	Y	注意格式: 09:25:00
# 板上成交额	int64	Y	-
# 连续跌停	int64	Y	-
# 开板次数	object	Y	-
# 所属行业	object	Y	-
# 接口示例

def query_dt_stock_pool(date=datetime.datetime.now().date()):
    date=utils.timeUtil.get_no_chaging_date(date)
    data = ak.stock_em_zt_pool_dtgc(date=date)
    date=datetime.datetime.now().date()
    data['date']=date
    print(data)
    return data

# 赚钱效应分析
# 接口: stock_legu_market_activity
#
# 目标地址: https://www.legulegu.com/stockdata/market-activity
#
# 描述: 获取乐咕乐股网-赚钱效应分析数据
#
# 限量: 单次返回当前赚钱效应分析数据
#
# 说明：
#
# 涨跌比：即沪深两市上涨个股所占比例，体现的是市场整体涨跌，占比越大则代表大部分个股表现活跃。
# 涨停板数与跌停板数的意义：涨停家数在一定程度上反映了市场的投机氛围。当涨停家数越多，则市场的多头氛围越强。真实涨停是非一字无量涨停。真实跌停是非一字无量跌停。
# 输入参数
#
# 名称	类型	必选	描述
# -	-	-	-
# 输出参数
#
# 名称	类型	默认显示	描述
# item	object	Y	-
# value	object	Y	-
# 接口示例

import akshare as ak
def query_earn_market():
    data = ak.stock_legu_market_activity()
    date=datetime.datetime.now().date()
    data['date']=date
    return data
# print(stock_legu_market_activity_df)





