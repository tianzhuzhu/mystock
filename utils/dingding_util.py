import datetime

import pandas as pd
from dingtalkchatbot.chatbot import DingtalkChatbot
# WebHook地址
import configger

webhook = 'https://oapi.dingtalk.com/robot/send?access_token=309e9334da6162c0ccac042b792deefb95be719503a2728946eec403d77e7a0c'
# secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 可选：创建机器人勾选“加签”选项时使用
# 初始化机器人小丁
ding = DingtalkChatbot(webhook)  # 方式一：通常初始化方式
# ding = DingtalkChatbot(webhook, secret=secret)  # 方式二：勾选“加签”选项时使用（v1.5以上新功能）
# ding = DingtalkChatbot(webhook, pc_slide=True)  # 方式三：设置消息链接在PC端侧边栏打开（v1.5以上新功能）
# Text消息@所有人

def send_messsage_byexcel(data:pd.DataFrame):
    msg='老大'
    columns=data.columns
    i =0
    for column in columns:
        data.sort_values(by=[column],ascending=True,inplace=True)
        indexs=(data[:3]).index.tolist()
        values=(data[:3][column]).tolist()
        print(indexs)
        print(values)
        for i in range(3):
            msg+='{}涨幅第{}的是{},涨幅为{}\r\n'.format(column,i+1,indexs[i],format(values[i], '.2%'))
        msg+='\r\n'

    ding.send_text(msg=msg, is_at_all=True)
    i = i + 1
    msg = '老大'
    for column in data.columns:
        data.sort_values(by=[column], ascending=False, inplace=True)
        indexs = (data[:3]).index.tolist()
        values = (data[:3][column]).tolist()
        print(indexs)
        print(values)
        for i in range(3):
            msg+='{}涨幅第{}的是{},涨幅为{}\r\n'.format(column,i+1,indexs[i],format(values[i], '.2%'))
        msg += '\r\n'
    ding.send_text(msg=msg, is_at_all=True)
    i = i + 1
def send_recent_forecat_byexcel(days=[3,7]):
    msg='老大'
    for day in days:
        sql="select * from tb_ak_bi_forecast_report where" \
            "(code like 'sh.%%' or code like 'sz.%%')  and" \
            " TIMESTAMPDIFF(DAY ,公告日期,(select max(公告日期) from tb_ak_bi_forecast_report )) >={}" .format(day)
        print(sql)
        engine=configger.getEngine()
        data=pd.read_sql(sql=sql,con=engine)
        data['业绩变动幅度'].fillna(0,inplace=True)
        data.sort_values(by=['业绩变动幅度'],inplace=True,ascending=False)
        count=data['业绩变动幅度'].count()
        print(count)
        data['temp']=data['股票简称']+'('+data['code']+')'
        str1=','.join(data['temp'].tolist())
        resstr='今天(%{}),近{}天更新的业绩共有{}条，详细如下:\r\n'.format(datetime.datetime.now().date(),day,count)
        resstr+=str1
        data['res']=data['temp']+':'+data['业绩变动幅度'].str
        res=data[0:3]
        str2='，'.join(res['res'].tolist())
        resstr+='业绩增幅前三的股票有{}'.format(str2)
        ding.send_text(msg=resstr)

send_recent_forecat_byexcel()