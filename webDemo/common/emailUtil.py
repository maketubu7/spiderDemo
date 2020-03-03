# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 15:40
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : emailUtil.py
# @Software: PyCharm
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import traceback


nickname = 'make'
username = 'dengwenxingae86@163.com'
password = 'dx045002'
to_username = 'dengwenxingae61@163.com'
to_list = ['dengwenxingae86@163.com']

class emailUtil(object):

    def __init__(self,username,password):
        ##连接SMTP服务器
        self.client = smtplib.SMTP("smtp.163.com")
        ##开启ssl
        self.client.starttls()
        ##登陆邮箱 用开启smtp服务的客户端授权密码
        self.client.login(user=username,password=password)
        ##创建邮件对象
        self.emailMsg = MIMEMultipart()
        self.image_file_suffix = ['.png','.jpg','.jpeg']
        self.other_file_suffix = ['.doc','.docx','.pdf','.xlsx','.xls','csv','.zip','.rar']
        self.file_suffix = self.image_file_suffix+self.other_file_suffix

    def add_attachment(self,filename):
        '''
        调用该方法依次添加附件
        :param filename: 需要发送附件的文件地址
        :return: none
        '''
        file_suffix = os.path.splitext(filename)[1]
        assert file_suffix in self.file_suffix, 'file type is not allow'
        Apart = None
        try:
            if file_suffix in self.image_file_suffix:
                Apart = MIMEImage(open(filename, 'rb').read(), filename.split('.')[-1])
                Apart.add_header('Content-Disposition', 'attachment', filename=filename)
            if file_suffix in self.file_suffix:
                Apart = MIMEApplication(open(filename, 'rb').read())
                Apart.add_header('Content-Disposition', 'attachment', filename=filename)
            if Apart:
                print("add Apart success filename: {}".format(filename))
                self.emailMsg.attach(Apart)
        except Exception as e:
            print(e)
            return


    def send_email(self,to_address,header_content='',text_content=''):
        '''
        添加主题 发送邮件
        :param to_address: [address1,address2,....]
        :param header_content: header text
        :param text_content: text content
        :return:
        '''
        self.emailMsg["Cc"] = 'dengwenxingae61@163.com;'
        self.emailMsg["Subject"] = Header(header_content,"utf-8") ##主题
        self.emailMsg["From"] = '{}<{}>'.format(nickname,username) ##发送者
        # emailMsg["To"] = to_username  ##接收者
        content = MIMEText(text_content,"plain","utf-8")  ##邮件内容
        content_html = MIMEText('我是超文本', _subtype='html', _charset='UTF-8')
        self.emailMsg.attach(content)  ##将内容添加到邮件
        self.emailMsg.attach(content_html)  ##将内容添加到邮件
        try:
        ##发送邮件到to_address的每个地址 to_address为包含每个接受地址的列表
            self.client.sendmail(username,to_address,self.emailMsg.as_string())
        except smtplib.SMTPRecipientsRefused:
            print('邮件发送失败，收件人被拒绝')
        except smtplib.SMTPAuthenticationError:
            print('邮件发送失败，认证错误')
        except smtplib.SMTPSenderRefused:
            print('邮件发送失败，发件人被拒绝')
        except smtplib.SMTPException as e:
            print('邮件发送失败, ',traceback.format_exc(e))
        finally:
            self.client.close()

if __name__ == '__main__':
    client = HandleSendEmail()
    client.add_attachment('F:\\maketubu\\时光\\网易云音乐相册\\54241090.jpg')
    client.add_attachment('E:\\区块链\\master_bitcoin.pdf')
    client.send_email(to_list,header_content='测试邮件',text_content='海边的曼彻斯特')

