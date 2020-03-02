# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 18:10
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseDemo.py
# @Software: PyCharm
import requests
import re,time

def demo1():
    response = requests.get(url="https://httpbin.org/ip")
    response = requests.get(url="https://www.qq.com")
    print(response.text)

def demo2():
    ##构造发送的数据
    data = {"name":"imooc"}
    ##发送post请求，data关键字，data参数
    response = requests.post(url="https://httpbin.org/post",data=data)
    ##查看返回数据
    print(response.text)

def demo3():
    ##设置网站证书
    url = 'https://requestb.in/'
    response = requests.get(url=url,)
    print(response.text)

def demo4():
    ##构造url
    url="https://httpbin.org/get"
    ##定义浏览器的请求头
    header = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    data = {"name":"make","age":23}
    ##通过params构造参数
    response = requests.get(url=url,params=data,headers=header)
    ##https://httpbin.org/get?name=make&age=23
    print(response.url)
    ##请求头
    print(response.headers)
    print(response.text)
    ##状态码
    print(response.status_code)
    ##请求头
    print(response.request.headers)
def demo5():
    ##请求图片数据
    url = 'https://www.imooc.com/templates/img/index/logo.png'
    response = requests.get(url=url)
    ##返回的二进制数据
    with open("imooc.png","wb") as f:
        f.write(response.content)

def demo6():
    ##解析json数据
    url = "https://httpbin.org/ip"
    response = requests.get(url=url)
    data = response.json()
    print(data["origin"])


def demo7():
    ##请求超时控制 timeou=time 控制连接时间
    url = 'http://www.github.com'
    response = requests.get(url=url,timeout=3)
    print(response.status_code)
    print(response.text)

def demo8():
    ##查看cookie
    url = 'http://www.baidu.com'

    ##定制请求头 设置了一个标准浏览器的UA
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }
    response = requests.get(url=url, headers=header)
    # response = requests.get(url=url)
    ##cookie是一个对象 RequestsCookieJar 行为和字典类似
    cookie = response.cookies
    print(cookie)
    print(cookie["H_PS_PSSID"])

def demo9():
    ##可查看当前发送cookie的url
    url = "http://httpbin.org/cookies"
    cookies = dict(cookies_are="hello imooc")
    ##设置cookies 通过cookies=cookies来给定
    response = requests.get(url=url,cookies=cookies)
    print(response.text)

def demo10():
    ##session设置
    url = 'http://account.chinaunix.net/login'
    header = {
        "Host": "account.chinaunix.net",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    ##构造session
    login_session = requests.session()
    ##<input type="hidden" name="_token" value="gl605XtLQxZ6gOvEdVfvwswYSFDRnwsQUajKV7fb">
    ##构造token的正则表达式
    token_search = re.compile(r'name="_token" value="(.*?)"')
    index_response = login_session.get(url=url,headers=header)
    # print(index_response.text)
    token_value = re.search(token_search,index_response.text).group(1)
    print(token_value)
    ##开始构造登陆的数据
    data = {
        "username":"maketubu",
        "password":"dx818514",
        "_token":token_value,
        "_t":int(time.time())   ##就是时间戳
    }
    ##d登陆使用的url
    login_url = "http://account.chinaunix.net/login/login"
    ##使用post请求
    login_reponse = login_session.post(url=login_url,headers=header,data=data)
    print(login_reponse.text)

    ##请求设置页面
    phone_url = 'http://account.chinaunix.net/ucenter/user/index'
    phone_response = login_session.get(url=phone_url,headers=header)
    ##可以看到设置页面的手机号码
    print(phone_response.text)

if __name__ == "__main__":
    demo10()