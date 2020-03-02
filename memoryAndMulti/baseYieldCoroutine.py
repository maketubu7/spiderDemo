# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 13:31
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseYieldCoroutine.py
# @Software: PyCharm

'''通过yield关键字实现协程'''

def count_down(n):
    while n > 0:
        yield n
        n -= 1

def yield_test():
    while True:
        n = (yield )
        print(n)

if __name__ == "__main__":
    # rest = count_down(5)
    # print(next(rest))
    # print(next(rest))
    # print(next(rest))
    # print(next(rest))
    # print(next(rest))
    reset = yield_test()
    reset.send('666')
    reset.send('666')