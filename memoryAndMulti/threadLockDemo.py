# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:37
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : threadLockDemo.py
# @Software: PyCharm
import threading


balance = 0
lock = threading.Lock()
rlock = threading.RLock()

def change_it(n):
    global balance
    ##添加锁
    try:
        lock.acquire()
        balance += n
        balance -= n
        print(threading.current_thread().name,'>>>>>>>>>>>>> ',balance)
        ##释放锁
    finally:
        lock.release()

def change_it2(n):
    global balance
    # 添加锁
    with lock:
        balance += n
        balance -= n
        print(threading.current_thread().name,'>>>>>>>>>>>>> ',balance)


class mythread(threading.Thread):

    def __init__(self, num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num = num
        self.name = 'thread_%s'%str(num)

    def run(self) -> None:
        for _ in range(10000):
            change_it2(self.num)

if __name__ == "__main__":
    t1 = mythread(5)
    t2 = mythread(8)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)