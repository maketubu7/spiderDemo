# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 14:40
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseAsyncIOCoroutine.py
# @Software: PyCharm
from asyncio import Queue
import asyncio

async def add(store,name):
    for i in range(5):
        await asyncio.sleep(1)
        await store.put(i)
        print('{} add one {} >>>> size {}'.format(name,i, store.qsize()))




async def reduce(store):
    for i in range(10):
        reset  = await store.get()
        print('reduce one {} <<<< size {}'.format(reset, store.qsize()))

def demo():
    q = Queue()

    event1 = add(q,'a')
    event2 = add(q,'b')
    r1 = reduce(q)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(event1,event2,r1))
    loop.close()

if __name__ == "__main__":
    demo()