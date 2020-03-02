# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 0:56
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : multiThreadDemo2.py
# @Software: PyCharm
import time
import threading
from multiprocessing.dummy import Pool
from concurrent.futures import ThreadPoolExecutor

def run(i):
    time.sleep(2)
    print(threading.current_thread().name)

def main():
    t1 = time.time()
    for _ in range(10):
        run(_)
    print(time.time()-t1)

def main_use_thread():

    t1 = time.time()
    ls = []
    for _ in range(10):
        for _ in range(10):
            t = threading.Thread(target=run,args=(_,))
            ls.append(t)
            t.start()
        for t in ls:
            t.join()
    print(time.time()-t1)

def main_use_pool():
    """使用线程池优化"""
    t1 = time.time()
    nlist = range(100)
    pool = Pool(10)
    pool.map(run,nlist)
    pool.close()
    pool.join()
    print(time.time()-t1)

def main_use_executor():
    """使用Executor优化"""
    t1 = time.time()
    nlist = range(100)
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(run,nlist)
    print(time.time() - t1)



if __name__ == "__main__":
    # main()
    # main_use_thread()
    # main_use_pool()
    main_use_executor()