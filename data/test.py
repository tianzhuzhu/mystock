# import tushare as ts
#
# # ts.get_hist_data('600848') #一次性获取全部日k线数据
# # print(ts.get_industry_classified())
# print(ts.get_stock_basics())
import myemail.send

if __name__ == '__main__':
    myemail.send.send_mail('a.txt')