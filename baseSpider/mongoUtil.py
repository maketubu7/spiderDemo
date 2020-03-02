# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 16:23
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : mongoUtil.py
# @Software: PyCharm
from pymongo import MongoClient
from common.libs.PropertiesUtil import Properties

props = Properties("mongo.properties").properties
class mongeClint(object):
    def __init__(self):
        __client = MongoClient(host=props["host"], port=int(props["port"]))
        __client.admin.authenticate(props["user"], props["password"])
        self.__mydb = __client["db_51job"]


    def insert_data(self,item):
        self.__mydb.collection_51job.insert_many(item)
        print('insert success')

mongo_client = mongeClint()

if __name__ == '__main__':
    mongo_client.insert_data([{"hah":"asd"}])
