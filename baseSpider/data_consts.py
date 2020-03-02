# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 14:44
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : data_consts.py
# @Software: PyCharm
from pymongo import MongoClient
from common.libs.PropertiesUtil import Properties

props = Properties("mongo.properties").properties
client =MongoClient(host=props["host"],port=int(props["port"]))
client.admin.authenticate(props["user"],props["password"])
mydb = client["db_51job"]

url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

header = {
    "Host":"search.51job.com",
    "Connection":"keep-alive",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8"
}

proxy = {
        "http":"http://HMKWGT4450117A4D:B08155EF494A67D7@http-dyn.abuyun.com:9020",
        "https":"http://HMKWGT4450117A4D:B08155EF494A67D7@http-dyn.abuyun.com:9020",
    }
