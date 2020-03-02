# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 10:28
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : HTTP_SERVER1.py
# @Software: PyCharm
import socket
import multiprocessing

def handle_client(client):
    #接收客户端数据
    client_data = client.recv(1024)
    print("client data: %s"%client_data)
    ##向客户端响应请求
    #状态行 包含HTTP的版本 状态码和状态描述 以空格分隔
    response_start_line = "HTTP/1.1 200 OK \r\n"
    #自定义响应头
    response_headers = "Server:my server\r\n"
    response_body = "Hello Make"
    response = response_start_line + response_headers + '\r\n' + response_body
    #回复二进制数据
    client.send(response.encode('utf-8'))
    print('server data:\r\n %s'%response)
    client.close()


def create_http():
    ##创建一个TCP类型的HTTP服务器
    server = socket.socket(type=socket.SOCK_STREAM)
    ##如果地址里面什么都不写，代表绑定的是当前机器的所有ip
    server.bind(("",8080))
    #服务端监听
    server.listen(128)
    print('wait connectiong....')
    ##接收客户端请求，返回客户端socket和客户端地址信息
    while True:    ##一直接收
        client,address = server.accept()
        print("client:",address[0],address[1])
        ##引入多进程，处理客户端的请求
        client_process = multiprocessing.Process(target=handle_client,args=(client,))
        ##开启jincheng
        client_process.start()

if __name__ == "__main__":
    create_http()