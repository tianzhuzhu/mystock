import datetime

import akshare as ak
#indicator	str	Y	indicator="沪股通"; 三选一 ("沪股通", "深股通", "北上")
# import akshare as ak
# stock_em_comment_df = ak.stock_em_comment()
# print(stock_em_comment_df)
import database
from utils.pdUtil import get_code_by_number


def query_north_net_in(indicator="北上"):
    data = ak.stock_em_hsgt_north_net_flow_in(indicator=indicator)
    data['indicator']=indicator
    return data

#indicator="沪股通"; 三选一 ("沪股通", "深股通", "北上")
def query_north_net_balance(indicator="北上"):
    data  = ak.stock_em_hsgt_north_cash(indicator=indicator)
    data['indicator']=indicator
    return data

#indicator	str	Y	indicator="沪股通"; 三选一 ("沪股通", "深股通", "北上")
def query_north_acc_flow_in(indicator="北上"):
    data = ak.stock_em_hsgt_north_acc_flow_in(indicator=indicator)
    data['indicator']=indicator
    return data

# indicator="沪股通"; choice of {"沪股通", "深股通", "南下"}
def query_south_net_flow_in(indicator="南下"):
    data = ak.stock_em_hsgt_south_net_flow_in(indicator=indicator)
    data['indicator']=indicator
    return data

# indicator="沪股通"; choice of {"沪股通", "深股通", "南下"}
def query_south_net_blance(indicator="南下"):
    data = ak.stock_em_hsgt_south_cash(indicator=indicator)
    data['indicator']=indicator
    return data

def query_south_acc_flow_in(indicator="南下"):
    data = ak.stock_em_hsgt_south_acc_flow_in(indicator=indicator)
    data['indicator']=indicator
    return data

#板块排行
#symbol="北向资金增持行业板块排行"; choice of {"北向资金增持行业板块排行", "北向资金增持概念板块排行", "北向资金增持地域板块排行"}
#indicator="今日"; choice of {"今日", "3日", "5日", "10日", "1月", "1季", "1年"}

def query_north_board_rank(symbol='北向资金增持行业板块排行',indicator='今日'):
    data = ak.stock_em_hsgt_board_rank(symbol=symbol, indicator=indicator)
    data['symbol'] = symbol
    data['indicator']=indicator
    return data
# 个股排行
# market	str	Y	market="沪股通"; choice of {"北向", "沪股通", "深股通"}
# indicator	str	Y	indicator="沪股通"; choice of {"今日排行", "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"}
def query_north_hold_stock(market='北向',indicator='今日排行'):
    data = ak.stock_em_hsgt_hold_stock(market=market, indicator=indicator)
    data['market'] = market
    data['indicator']=indicator
    return data

#每日个股统计
# 接口: stock_em_hsgt_stock_statistics
#
# 目标地址: http://data.eastmoney.com/hsgtcg/StockStatistics.aspx
#
# 描述: 获取东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
#
# 限量: 单次获取指定 market 的所有数据
#
# 输入参数
#
# 名称	类型	必选	描述
# symbol	str	Y	symbol="北向持股"; choice of {"北向持股", "沪股通持股", "深股通持股", "南向持股"}
# start_date	str	Y	start_date="20210601"; 此处指定近期交易日
# end_date	str	Y	end_date="20210608"; 此处指定近期交易日


def every_day_stock_statistics(symbol='北向持股',start_date='19910101',end_date='20201218'):
    data = ak.stock_em_hsgt_stock_statistics(symbol=symbol, start_date=start_date, end_date=end_date)
    data['symbol']=symbol
    return data


# 每日机构统计
# 接口: stock_em_hsgt_institution_statistics
#
# 目标地址: http://data.eastmoney.com/hsgtcg/InstitutionStatistics.aspx
#
# 描述: 获取东方财富网-数据中心-沪深港通-沪深港通持股-每日机构统计
#
# 限量: 单次获取指定 market 的所有数据
#
# 输入参数
#
# 名称	类型	必选	描述
# market	str	Y	market="北向持股"; choice of {"北向持股", "沪股通持股", "深股通持股", "南向
def every_day_insititution_statistics(market,start_date,end_date):
    data = ak.stock_em_hsgt_institution_statistics(market=market,
                                                                                      start_date=start_date,
                                                                                      end_date=end_date)
    return data


# 沪深港通历史数据
# 接口: stock_em_hsgt_hist
#
# 目标地址: http://data.eastmoney.com/hsgt/index.html
#
# 描述: 获取东方财富网-数据中心-资金流向-沪深港通资金流向-沪深港通历史数据
#
# 限量: 单次获取指定 market 的所有数据
#
# 输入参数
#
# 名称	类型	必选	描述
# symbol	str	Y	symbol="港股通沪"; choice of {"沪股通", "深股通", "港股通沪", "港股通深"}

def shsz_history_data(symbol):
    data = ak.stock_em_hsgt_hist(symbol=symbol)
    return data

def save_north_data(hold_stock_table='tb_ak_north_hold_stock',hold_board_rank_table='tb_ak_north_board_rank',way='byboot'):
    database.init()
    engine=database.engine
    # north_net_in=query_north_net_in()#北上资金净流入
    # north_cash_balance=query_north_net_balance()#北上资金净流入
    # north_cash_acc_flow_in=query_north_acc_flow_in()
    symbol_list=["北向资金增持行业板块排行", "北向资金增持概念板块排行", "北向资金增持地域板块排行"]
    market_list=["北向", "沪股通", "深股通"]
    indicator_list=["今日排行", "3日排行", "5日排行", "10日排行", "月排行", "季排行", "年排行"]
    for market in market_list:
        for indicator in indicator_list:
            hold_stock = query_north_hold_stock(market,indicator)
            hold_stock=get_code_by_number(hold_stock,'代码')
            hold_stock['updatetime']=datetime.datetime.now().date()
            print(hold_stock)
            hold_stock.to_sql(hold_stock_table,con=engine,index=False,if_exists='append')
    indicator_list = ["今日", "3日", "5日", "10日", "1月", "1季", "1年"]
    for symbol in symbol_list:
        for indicator in indicator_list:
            board_rank=query_north_board_rank(symbol,indicator)
            board_rank['updatetime']=datetime.datetime.now().date()
            board_rank=get_code_by_number(board_rank,'代码')
            print(board_rank)
            board_rank.to_sql(hold_board_rank_table,con=engine,index=False,if_exists='append')
if __name__=='__main__':
    save_north_data()

