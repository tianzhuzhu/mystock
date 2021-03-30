import os
import smtplib
import datetime
import pandas as pd
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import plotUtil.plotDay
import plotUtil.plotDayNew
def send(filepath):
    #第三方SMTP服务
    mail_host="smtp.163.com" #设置服务器
    mail_user="lujin19950917@163.com"  #用户名
    mail_pass="SAQCPCVSXLCVKHDT"  #口令
    today=datetime.datetime.now().date()
    sender = 'lujin19950917@163.com' # 发送方
    receivers = ['lujin19950917@163.com','532978773@qq.com','617970137@qq.com','893573580@qq.com','3082872656@qq.com'] # 接收方

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '{}您好！根据pe和增长结果如下:请看如下附件'.format(today)
    #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
    # 邮件内容

    # 发送当前目录下的 Spring Boot实战 ,丁雪丰 (译者) .pdf 文件
    print(filepath)


    pfile = '结果{}.xlsx'.format(today)
    pdffile = MIMEApplication(open(filepath,'rb').read())
    pdffile.add_header('Content-Disposition','attachment',filename=pfile)
    txt = MIMEText('这是{}所有的股票列表，请查收！'.format(today), 'plain', 'utf-8')
    message.attach(txt)
    #将附件内容插入邮件中
    message.attach(pdffile)

    #登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        print('success')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error',e)



def send_mail(filelist,namelist,data):
    #第三方SMTP服务
    print('send','邮件开始')
    klinePath=data['path']['default-kLine']
    date=datetime.datetime.now().date()

    path=os.path.join(klinePath,str(date))
    if(not os.path.exists(path)):
        os.mkdir(path)

    mail_host="smtp.163.com" #设置服务器
    mail_user="lujin19950917@163.com"  #用户名
    mail_pass="SAQCPCVSXLCVKHDT"  #口令
    today=datetime.datetime.now().date()
    sender = 'lujin19950917@163.com' # 发送方
    receivers = ['lujin19950917@163.com','532978773@qq.com','617970137@qq.com','893573580@qq.com'] # 接收方

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receivers[0]
    message['Subject'] = '{}您好！根据pe和增长结果如下:请看如下附件'.format(today)
    #推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
    # 邮件内容
    txt = MIMEText('这是{}所有的股票列表，请查收！'.format(today), 'plain', 'utf-8')
    message.attach(txt)

    # 发送当前目录下的 Spring Boot实战 ,丁雪丰 (译者) .pdf 文件
    for i in range(len(filelist)):
        filepath=filelist[i]
        name=namelist[i]
        # pfile = '结果{}.xlsx'.format(today)
        print(name,filepath)
        data=pd.read_excel(filepath,sheet_name=0)
        code=data['code'].iloc[0]
        print(code)
        klinePath=os.path.join(path,code+'.jpg')
        figPath=plotUtil.plotDayNew.plotK(klinePath,'日线',code)

        pdffile = MIMEApplication(open(filepath,'rb').read())
        pdffile.add_header('Content-Disposition','attachment',filename=name)
        #将附件内容插入邮件中
        message.attach(pdffile)
#附件设置内容类型，方便起见，设置为二进制流
        content2 = MIMEText(namelist[i])
        # part2 = MIMEText(content2,'plain','utf-8')
        # part2['Content-Type'] = 'application/octet-stream'
        #设置附件头，添加文件名
        # part2['Content-Disposition'] = 'attachment;filename="abc.txt"'
        with open(figPath,'rb') as fp:
            picture = MIMEImage(fp.read())
            #与txt文件设置相似
            picture['Content-Type'] = 'application/octet-stream'
            picture['Content-Disposition'] = 'attachment;filename={}.jpg'.format(code)
#将内容附加到邮件主体中
            # message.attach(part2)
            message.attach(content2)
            message.attach(picture)
        # msgRoot = MIMEMultipart('related')
        # msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.'
        #                    '<img src="cid:figPath">' \
        #                    # '<img src="cid:figPath">' \
        #                    # '<img src="cid:image3">' \
        #                    'good!', 'html', 'utf-8')
        # msgRoot.attach(msgText)
        # message.attach(msgRoot)
    #登录并发送
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        print('success')
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print('error',e)
if __name__=='__main__':
    send_mail(['a.xlsx'],['结果'])
