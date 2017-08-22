#!/usr/bin/env python
# coding:utf-8

import smtplib
from email.mime.text import MIMEText
class sendmail(object):
    def __init__(self):
        # 设置服务器所需信息
        # 163邮箱服务器地址
        self.mail_host = 'smtp.shuhua.com'
        # 163用户名
        self.mail_user = 'liqingy'
        # 密码(部分邮箱为授权码)
        self.mail_pass = 'Liqy2122'
        # 邮件发送方邮箱地址
        self.sender = 'liqingy@shuhua.com'

    def mail(self, title, content):
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = ['79138790@qq.com', 'a-lu@outlook.com']
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = receivers[0]
        self.send(receivers,message)

    def send(self, receivers, message):
        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            smtpObj.connect(self.mail_host, 25)
            # 登录到服务器
            smtpObj.login(self.mail_user, self.mail_pass)
            # 发送
            smtpObj.sendmail(
                self.sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('success')
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误

