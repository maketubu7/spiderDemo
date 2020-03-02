# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 1:27
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseProcessDemo.py
# @Software: PyCharm
import sys,os,time
from multiprocessing import Process,Queue


def run(name):
    print(name,os.getpid())
    time.sleep(40)
    print('>>')

class myprocess(Process):

    def __init__(self,name,*args,**kwags):
        super().__init__(*args,**kwags)
        self.name  = name

    def run(self):
        print(self.name, os.getpid())
        time.sleep(1)
        print('>>')

class write_process(Process):

    def __init__(self,q,*args,**kwags):
        super().__init__(*args,**kwags)
        self.q  = q

    def run(self):
        '''实现进程的业务逻辑'''
        ls = [str(_) for _ in range(3)]
        for line in ls:
            self.q.put(line)
            time.sleep(2)

class read_process(Process):

    def __init__(self,q,*args,**kwags):
        super().__init__(*args,**kwags)
        self.q  = q

    def run(self):
        '''实现进程的业务逻辑'''
        while True:
            content = self.q.get()
            print(content)


if __name__ == "__main__":
    # p = Process(target=run,args=("my",))
    ##通过queue共享数据
    q = Queue()
    p_write = write_process(q)
    p_write.start()
    p_read = read_process(q)
    p_read.start()
    p_write.join()
    # p_write.join()

    ##读的进程是死循环
    p_read.terminate()