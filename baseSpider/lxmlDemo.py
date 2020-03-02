# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 11:57
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : lxmlDemo.py
# @Software: PyCharm
from lxml import etree

##html数据
html_data = '''
<div>
  <ul>
       <li class="item-0"><a href="link1.html">first item</a></li>
       <li class="item-1"><a href="link2.html">second item</a></li>
       <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
       <li class="item-1"><a href="link4.html">fourth item</a></li>
       <li class="item-0"><a href="link5.html">fifth item</a>
   </ul>
</div>
'''

def demo1():
    ##使用etree转为html格式 返回为etree._Element为整个xml树的根节点
    html = etree.HTML(html_data)
    ##通过tostring()转为字节，在编码
    print(etree.tostring(html).decode())
    print(type(html))

def demo2():
    ##xpath
    html = etree.HTML(html_data)
    ##这样返回的是一个列表，每一个元素都是element类型
    ##每一个element就代表一个标签元素
    res = html.xpath('//li/a/text()')   #['first item', 'second item', 'fourth item', 'fifth item']
    print(res)
    ##获取所有的元素下 class的属性值
    res = html.xpath('//li/@class')  #['item-0', 'item-1', 'item-inactive', 'item-1', 'item-0']
    print(res)

    ##获取li标签href值为link1.html这个a标签的值
    res = html.xpath('//li/a[@href="link1.html"]/text()')  # ['first item']
    print(res)

    ##获取li标签下 a标签中的 span标签的值
    res = html.xpath('//li//span/text()')  # ['first item']
    print(res)

    ##获取li标签下 最后一个元素的a标签中的 href的值
    res = html.xpath('//li[last()]/a/@href')  # ['first item']
    print(res)


def demo3():
    ##爬取求职信息 51job
    pass
if __name__ == "__main__":
    demo2()