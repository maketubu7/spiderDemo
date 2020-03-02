# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 22:06
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : UDP_CLIENT.py
# @Software: PyCharm
import socket
host = "127.0.0.1"
port = 1234
def create_client():
    client = socket.socket(type=socket.SOCK_DGRAM)
    send_data = input("in: ")
    client.sendto(send_data.encode(),(host,port))
    client_data,address = client.recvfrom(1024)
    print("服务端信息",client_data.decode('utf-8'))
    client.close()

if __name__ == "__main__":
    create_client()