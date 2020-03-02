# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 21:01
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : scapyXpathDemo.py
# @Software: PyCharm
from scrapy import Selector
import requests,re

url = 'http://127.0.0.1:1111'
response = requests.get(url=url)
html = response.text

def demo():
    ###就是lxml的xpath方法，只不过在这里做了封装
    sel = Selector(text=html)
    tag = sel.xpath("//div[@id='info']/div/p[1]/text()").extract()[0]
    print(tag)

if __name__ == "__main__":
    demo()