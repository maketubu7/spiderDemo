# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 22:26
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : talk_server.py
# @Software: PyCharm
import socket
import time

host = "127.0.0.1"
port = 1234
def create_server():

    server = socket.socket(type=socket.SOCK_DGRAM)
    server.bind((host,port))
    print("wait connection.....")
    nickname = input("nickname: ")

    while True:
        data,address = server.recvfrom(1024)
        data = data.decode().split("#")
        print(data[0] + ": " + data[1])
        send_msg = input("%s: "%nickname)
        msg = "{}#{}".format(nickname,send_msg).encode('utf-8')
        if send_msg == "quit":
            server.sendto(msg, address)
            break
        server.sendto(msg,address)
        # print(nickname + ": " + send_msg)
        # server.close()

if __name__ == '__main__':
    create_server()