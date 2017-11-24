#!/usr/bin/env python3
#coding=utf-8


import os
import sys
import time
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

current_path = os.path.abspath(os.path.dirname(__file__)) + os.sep
sys.path.append(current_path)
import conf

class SendMail():

    def __init__(self,mail_server,user,pwd):
        self.user = user
        server = smtplib.SMTP()
        server.connect(mail_server,"25")
        server.login(user, pwd)
        self.server = server

    def send(self,to='',cc='',subject='',content='',attach=''):
        msg = MIMEMultipart()
        msg['From'] = 'auto_test' + '<' + self.user + '>'
        msg['To'] = ','.join(to)
        msg['Cc'] = ','.join(cc)
        
        msg['Subject'] = subject
        mail_list = to + cc

        # 邮件显示内容
        text_msg = MIMEText(content, 'plain', 'utf-8')
        msg.attach(text_msg)

        if attach:
            for i in attach:
                print(i)
                filename = os.path.basename(i)

                # 附件
                contype = 'application/octet-stream'
                maintype, subtype = contype.split('/', 1)

                ## 读入文件内容并格式化
                data = open(i, 'rb')
                file_msg = MIMEBase(maintype, subtype)
                file_msg.set_payload(data.read())
                data.close()
                email.encoders.encode_base64(file_msg)

                ## 设置附件头
                basename = os.path.basename(i)
                file_msg.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(file_msg)

        #self.server.set_debuglevel(1)
        self.server.sendmail(self.user, mail_list, msg.as_string())
        self.server.quit()

def sendmail(attach):
    '''发送测试报告'''
    subject = '接口测试结果：%s' % time.strftime('%Y/%m/%d %H:%M:%S')
    content = "接口测试已完成，测试详情请查看附件测试报告！"


    mail_server = conf.get_conf('mail','server')
    mail_user = conf.get_conf('mail','user')
    mail_passwd = conf.get_conf('mail','passwd')
    mail_to = eval(conf.get_conf('mail','to'))
    mail_cc = eval(conf.get_conf('mail','cc'))
    sendmail = SendMail(mail_server,mail_user,mail_passwd)
    sendmail.send(to=mail_to,cc=mail_cc,subject=subject,content=content,attach=[attach])


if __name__ == '__main__':
    sendmail('test')