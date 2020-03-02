# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 12:40
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseProcessLockDemo.py
# @Software: PyCharm
import time
from multiprocessing import Process, Lock


class write_process(Process):

    def __init__(self,filename,num,lock,*args,**kwags):
        super().__init__(*args,**kwags)
        self.filename = filename
        self.num = num
        self.lock = lock

    def run(self):
        '''实现进程的业务逻辑'''
        try:
            ##添加锁
            self.lock.acquire()
            for _ in range(5):
                content = '{} : {}\n'.format(self.name, self.num)
                time.sleep(2)
                print(content)
                with open(self.filename, 'a+') as f:
                    f.write(content)
        finally:
            ##释放锁
            self.lock.release()

class write_process2(Process):

    def __init__(self,filename,num,lock,*args,**kwags):
        super().__init__(*args,**kwags)
        self.filename = filename
        self.num = num
        self.lock = lock

    def run(self):
        '''实现进程的业务逻辑'''
        with self.lock:
            for _ in range(5):
                content = '{} : {}\n'.format(self.name, self.num)
                time.sleep(2)
                print(content)
                with open(self.filename, 'a+') as f:
                    f.write(content)


if __name__ == "__main__":
    lock = Lock()
    for _ in range(5):
        t = write_process2('write_process.txt',_,lock)
        t.start()
