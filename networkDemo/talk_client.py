# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 22:26
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : talk_client.py
# @Software: PyCharm
import socket

host = "127.0.0.1"
port = 1234

def create_client():
    client = socket.socket(type=socket.SOCK_DGRAM)
    nickname = input("nickname: ")
    print("wait connection.....")
    while True:
        send_data = input("%s: "%nickname)
        msg = "{}#{}".format(nickname, send_data).encode('utf-8')
        if send_data == 'quit':
            client.sendto(msg,(host,port))
            break
        client.sendto(msg, (host, port))
        # print(nickname + ": " + send_data)
        data,address = client.recvfrom(1024)
        data = data.decode().split("#")
        print(data[0] + ": " + data[1])
        # client.close()

if __name__ == "__main__":
    create_client()