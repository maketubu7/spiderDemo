# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 10:28
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : HTTP_SERVER2.py
# @Software: PyCharm
import socket
import multiprocessing


HTML_DIR = "F:\spiderDemo\\networkDemo\\application_layer\http\\"

def handle_client(client):
    #接收客户端的数据
    client_request_data = client.recv(1024)
    print("客户端的请求数据为:%s"%client_request_data)
    #向客户端响应数据,是根据HTTP协议的规范的
    #状态行：包含 HTTP 协议版本、状态码和状态描述，以空格分隔
    response_start_line = "HTTP/1.1 200 OK\r\n"
    #自定义了一个响应头
    response_headers = "Server:My server\r\n"
    # response_body = "Hello World"
    #GET / HTTP/1.1\r\n
    #通过空格分割客户端的请求数据
    request_data = client_request_data.decode().split(" ")
    #拿到客户端要请求的文件
    if request_data[1] == "/":
        #index.html前面一定要加上斜杠
        filename = "/index.html"
    else:
        filename = request_data[1]
    #filename----index.html
    #客户端请求的是图片文件，视频文件
    try:
        #文件可以找到
        with open(HTML_DIR+filename,'rb') as f:
            response_body = f.read()
    except:
        #文件找不到
        response_start_line = "HTTP/1.1 404 Not Found\r\n"
        response_body = "File Not Found".encode("utf-8")
    #响应正文：返回内容，注意和响应头之间有一个空行
    response = response_start_line+response_headers+"\r\n"+response_body.decode()
    print("服务器响应的数据为:%s"%(response))
    #一定要回复二进制数据
    client.send(response.encode("utf-8"))
    client.close()


if __name__ == '__main__':
    #创建一个TCP类型的HTTP服务器
    server = socket.socket(type=socket.SOCK_STREAM)
    #如果地址里面什么都不写，代表绑定的是我当前机器的所有IP地址,ip地址和端口号是一个元祖
    server.bind(("",8080))
    #服务端监听
    server.listen(128)
    print("WEB服务器已经启动....")
    #不停的接收客户端的请求
    while True:
        #接收客户端的请求，并且返回两个信息，分比为客户端的socket和客户端的地址信息
        client,address = server.accept()
        print("%s,%s连接上了WEB服务器"%(address[0],address[1]))
        #引入多进程，处理多个客户端的请求
        client_process = multiprocessing.Process(target=handle_client,args=(client,))
        #开启进程
        client_process.start()