# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 20:05
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : beautifulSoupDemo.py
# @Software: PyCharm
from bs4 import BeautifulSoup
import requests,re

url = 'http://127.0.0.1:1111'
response = requests.get(url=url)
html = response.text
bs = BeautifulSoup(html,"html.parser")

def demo():
    data = {}
    title_tag = bs.title
    data["title_name"] = title_tag.name
    data["title"] = title_tag.string
    data["title_attr"] = title_tag.attrs

    # div_tag = bs.div
    # div_tags = bs.find_all('div')
    div_tag = bs.find('div')
    div_tag = bs.find(id = 'info')
    div_tag = bs.find("div",id = 'info')
    div_tag = bs.find("div",id = re.compile("info-\d+"))

    res = bs.find(string='tornado从入门到精通')
    res = bs.find(string=re.compile('\d{1,}\.?\d{1,}'))
    print(res)





    print(data)

def demo2():
    div_tag = bs.find("div", id=re.compile("info-\d+"))
    ##子元素
    # childrens = div_tag.contents
    ##子元素的子元素
    # childrens = div_tag.descendants
    # for child in childrens:
    #     if child.name:
    #         print(child.name)

    p_tag = bs.find('p',{"class":"name"})
    ##找到元素的父节点
    # p_tag_parent = p_tag.parent
    ##元素父元素的父元素 找到所有上级元素
    # p_tag_parent = p_tag.parents
    #
    # for parent in p_tag_parent:
    #     print(parent.name)
    ##获取本身之后的兄弟
    next_siblings = p_tag.next_siblings
    #获取本身之前的兄弟节点
    pre_siblings = p_tag.previous_siblings
    for item in next_siblings:
        if item.name:
            ##获取元素属性
            print(item.get("class"))
            print(item.string)
    for item in pre_siblings:
        if item.name:
            print(item.get("class"))  ##原生属性多个就返回列表形式，自定义属性 返回本身的字符串
            print(item.string)


if __name__ == "__main__":
    # demo()
    demo2()