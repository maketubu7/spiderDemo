# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:40
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : EMAIL_SERVER.py
# @Software: PyCharm
import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

nickname = 'make'
username = 'dengwenxingae86@163.com'
password = 'dx045002'
to_username = 'dengwenxingae61@163.com'
to_list = ['dengwenxingae86@163.com','dengwenxingae61@163.com']

class HandleSendEmail(object):

    def __init__(self):
        ##连接SMTP服务器
        self.client = smtplib.SMTP("smtp.163.com")
        ##开启ssl
        self.client.starttls()
        ##登陆邮箱 用开启服务的客户端授权密码
        self.client.login(user=username,password=password)

    def send_email(self,to_address):
        ##创建邮件对象
        emailMsg = MIMEMultipart()
        ##主题
        emailMsg["Subject"] = Header("love","utf-8")
        ##发送者
        emailMsg["From"] = '{}<{}>'.format(nickname,username)
        ##接收者
        # emailMsg["To"] = to_username
        ##邮件内容
        content = MIMEText("i love 61","plain","utf-8")
        ##将内容添加到邮件
        emailMsg.attach(content)

        ##发送邮件到to_address的每个地址
        self.client.sendmail(username,to_address,emailMsg.as_string())
        self.client.close()

if __name__ == '__main__':
    client = HandleSendEmail()
    client.send_email(to_list)

