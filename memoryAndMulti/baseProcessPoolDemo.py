# -*- coding: utf-8 -*-
# @Time    : 2020/2/27 13:07
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : baseProcessPoolDemo.py
# @Software: PyCharm
import sys,time,os
from multiprocessing import Process, current_process,Pool


def run(filename,num):
    '''
    :param filename:
    :param num:
    :return: 写入的结果提示
    '''
    try:
        with open(filename, 'a+', encoding='utf8') as f:
            content = '{} {} {}'.format(current_process().name, current_process().pid, num)
            print(content)
            f.write(content)
            f.write('\n')
            time.sleep(1)
    except Exception as e:
        print(e)
        return False
    return True



if __name__ == "__main__":
    # print(os.cpu_count())
    filename = 'write_process_pool.txt'
    ##进程池
    pool = Pool(2)
    reset_list = []
    for i in range(10):
        ##同步添加任务
        # reset = pool.apply(run,args=(filename,i))
        # print('{}>>>>>{}'.format(i, reset))
        ##异步添加任务 通过get拿到执行结果
        reset = pool.apply_async(run,args=(filename,i))
        reset_list.append(reset)
        # print('{}>>>>>{}'.format(i,reset.get(2)))

    ##关闭进程池防止添加
    pool.close()
    pool.join()

    ##查看异步执行的结果
    print([_.get() for _ in reset_list])
