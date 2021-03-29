import traceback

import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
# 登陆系统
from data import util
import datetime
if __name__ == '__main__':
    # myemail.send.send_mail('a.txt')
    lg = bs.login()
# 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    # 查询杜邦指数
    dupont_list = []
    rs_dupont = bs.query_dupont_data(code="sh.600000", year=2017, quarter=2)
    while (rs_dupont.error_code == '0') & rs_dupont.next():
        dupont_list.append(rs_dupont.get_row_data())
    result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)
    # 打印输出
    print(result_profit)
    # 结果集输出到csv文件
    result_profit.to_csv("D:\\dupont_data.csv", encoding="gbk", index=False)

    # 登出系统
    bs.logout()