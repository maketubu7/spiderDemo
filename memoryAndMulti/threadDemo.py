# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:10
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : threadDemo.py
# @Software: PyCharm
from threading import Thread
import threading,time
from typing import Optional


def loop():
    print(threading.current_thread().name)
    n = 0
    while n < 5:
        print(n)
        n += 1

def use_thread():
    print(threading.current_thread().name)
    t = Thread(target=loop,name='loop_thread')
    ##启动
    t.start()
    ##挂起
    t.join()


class my_thread(Thread):

    def __init__(self):
        super(my_thread,self).__init__()
        self.n = 0

    def run(self):
        while self.n < 5:
            print(self.n)
            print(threading.current_thread().name)
            time.sleep(1)
            self.n += 1

if __name__ == "__main__":
    # use_thread()

    t = my_thread()
    t.start()
    t.join()