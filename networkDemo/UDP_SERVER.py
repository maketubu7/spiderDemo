# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 22:05
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : UDP_SERVER.py
# @Software: PyCharm
import socket
import time


def create_server():
    ##创建socket 并指定位socket类型位UDP
    server = socket.socket(type=socket.SOCK_DGRAM)

    ##绑定类型 并设置端口号
    server.bind(('127.0.0.1',1234))

    print("wait connection.....")
    ##recvfrom 方法返回了客户端的地址与端口号，以及服务器端接收到数据
    ##1024代表了服务器接收的数据的长度
    data,address = server.recvfrom(1024)
    print("客户端信息",address[0],address[1],data)
    ##向客户端发送信息，address是前面捕获的地址信息
    server.sendto("make".encode('utf-8'),address)
    server.close()
    # time.sleep(1000)

if __name__ == '__main__':
    create_server()


