# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 13:49
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseAsyncCoroutine.py
# @Software: PyCharm
import asyncio

async def do_sth(x):
    print('wait',x)
    await asyncio.sleep(x)

def demo():
    coroutine = do_sth(5)
    ##事件的循环队列
    loop = asyncio.get_event_loop()
    ##注册任务
    task = loop.create_task(coroutine)
    print(task)
    ##等待协程任务执行结束
    loop.run_until_complete(task)
    print(task)


async def compute(x,y):
    assert isinstance(x,int), 'x只能为整数'
    assert isinstance(y,int), 'y只能为整数'
    print('computeing {}+{}'.format(x,y))
    await asyncio.sleep(4)
    return x+y

async def plrint_sum(x,y):
    res = await compute(x,y)
    print('{}+{}={}'.format(x,y,res))

def demo1():
    ##事件的循环队列
    loop = asyncio.get_event_loop()
    ##等待协程任务执行结束
    loop.run_until_complete(plrint_sum(5,4))
    loop.close()

if __name__ == "__main__":
    ##判断是否为协程函数
    # print(asyncio.iscoroutinefunction(do_sth))
    # demo()
    demo1()