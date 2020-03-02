# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 15:05
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : logUtil.py
# @Software: PyCharm
import pandas as pd
import numpy as np

class logUtil(object):

    @staticmethod
    def deallog(filename, usecols=None, columns=None, drop_key=None,sep=','):
        '''
        :param filename:
        :return:
        '''
        if not usecols:
            usecols = [1]
        if not columns:
            columns = ["phone"]
        usecols = [int(c) for c in usecols]
        assert len(usecols) == len(columns), 'usecols length must equal columns length'
        plist = []
        print(filename)
        with open(filename, 'r', encoding='utf8') as f:
            try:
                lines = f.readlines()
                for line in lines[1:]:
                    if line.startswith("#"):
                        continue
                    phone = [line.split(sep)[i] for i in usecols]
                    plist.append(phone)
            except:
                pass
            phones = pd.DataFrame(plist, columns=columns, index=None, dtype=np.str)
            if drop_key:
                phones.drop_duplicates(subset=drop_key, inplace=True)
            return phones

if __name__ == '__main__':
    filename = 'F:\\spiderDemo\\webDemo\\upload\\828136f1-03eb-4d1f-b959-031697c7e69c.log'
    usecols = [0,1,2,3,4]
    columns = ["0","1","2","3","4"]
    drop_key = ["1"]
    sep = ','
    df = logUtil.deallog(filename,usecols,columns,drop_key,sep)
    print(df.to_dict(orient='list'))
