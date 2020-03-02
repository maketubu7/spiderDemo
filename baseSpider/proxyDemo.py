# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:34
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : proxyDemo.py
# @Software: PyCharm
import requests

def proxyDemo():

    proxy = {
        "http":"http://HQC790AK70LH001D:EC24D8F348E7F73D@http-dyn.abuyun.com:9020",
        "https":"http://HQC790AK70LH001D:EC24D8F348E7F73D@http-dyn.abuyun.com:9020",
    }

    url = "http://httpbin.org/ip"

    for _ in range(5):
        ##设置代理得关键字 proxies
        response = requests.get(url=url,proxies=proxy)
        print(response.text)

if __name__ == "__main__":
    proxyDemo()