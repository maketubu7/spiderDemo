# -*- coding: utf-8 -*-
# @Time    : 2020/2/25 20:49
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : regexDemo.py
# @Software: PyCharm

import re

def demo1():
    pattern = re.compile(r"\d+")
    m1 = pattern.match('one123tow234')
    m2 = pattern.search('one123tow234')
    m3 = pattern.findall('one123tow234')

    print(m1)
    print(m2.group())
    print(m3)

def subDemo():
    s = 'asd45sd7sd2d0df45l213y'
    conver = lambda a: '9' if int(a.group()) > 5 else '0'
    res = re.sub('\d{2}', conver, s,1)  # sub  传入函数的示例
    print(res)

def splitDemo():
    ##通过 正则匹配的结果对字符串进行分隔
    pattern = re.compile(r"[\s\,\;]+")
    string = 'a,b;; c   d'
    print(pattern.split(string))


def groupDemo():
    string = '<h1 class="test">imooc</h1>'
    # 我们匹配数字
    pattern = re.compile('\d')
    #这里调用了re模块的sub,把h1标签里面的1换成了2
    print(pattern.sub('2',string))
    #这个count用来指定替换次数的,如果不指定，则为全文替换
    print(pattern.sub('2',string,1))
    # 分组乱入，使用了search方法来获取分组里面的数据，通过group()里面的数字，来
    # 确定分组,这个正则表达式，也在函数中用到了
    # .\d被后面的\1所引用,使用了命名分组方法，制定了一个名字，classname
    pattern = re.compile('<(.\d)\sclass="(?P<classname>.*?)">.*?</(\\1)>')
    # print(pattern.search(string).group(1))

    #定义一个函数,match对象
    def func(m):
        #取了第二个分组
        return 'after sub ' + m.group('classname')
    #调用sub方法
    print(pattern.sub(func,string))
    string = '<h1 class="test">imooc</h1>'
    # 使用了贪婪模式，匹配到了所有的字符串
    pattern1 = re.compile(r'<.\d\sclass=.*>')
    print(pattern1.search(string).group())
    # 关闭了贪婪模式，使用?
    pattern2 = re.compile(r'<.\d\sclass=.*?>')
    print(pattern2.search(string).group())


if __name__ == "__main__":
    # demo1()
    # subDemo()
    # splitDemo()
    groupDemo()