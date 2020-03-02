# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:25
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : multiThreadDemo.py
# @Software: PyCharm
import threading


balance = 0

def change_it(n):
    global balance
    balance += n
    balance -= n
    print(threading.current_thread().name,'>>>>>>>>>>>>> ',balance)

class mythread(threading.Thread):

    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = num
        self.name = 'thread_%s'%str(num)

    def run(self) -> None:
        for _ in range(100):
            change_it(self.num)



if __name__ == "__main__":
    t1 = mythread(5)
    t2 = mythread(8)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)