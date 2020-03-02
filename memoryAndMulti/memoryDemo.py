# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 22:01
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : memoryDemo.py
# @Software: PyCharm
import sys
import gc

def extend_list(val, l =[]):
    l.append(val)
    return l

def jvm():
    l = [1]
    print(sys.getrefcount(l))

def gcdemo():
    print(gc.get_threshold())

if __name__ == "__main__":
    l1 = extend_list(10)
    l2 = extend_list(123,[])
    l3 = extend_list('a')

    jvm()
    gcdemo()