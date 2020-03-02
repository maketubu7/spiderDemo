# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 14:41
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : spider2mongo.py
# @Software: PyCharm
from baseSpider.data_consts import *
import requests,json
from lxml import etree
import re


def dealSalary(salary_desc):
    if salary_desc:
        patterm = re.compile(r'\d+\.?\d*')
        res = patterm.findall(salary_desc)
        res = sorted([float(i) for i in res])
        if '万' in salary_desc:
            res = [int(i*10000) for i in res]
            return tuple(res)
        if 'k' in salary_desc.lower():
            res = [int(i*1000) for i in res]
            return tuple(res)
        return tuple([int(i) for i in res])
    else:
        return (0,0)


def demo():
    response = requests.get(url=url,headers=header)
    response.encoding = 'gbk'
    # print(response.text)
    html_51 = etree.HTML(response.text)
    all_div = html_51.xpath("//div[@id='resultList']//div[@class='el']")
    info_list = []
    # print(all_div[1].xpath("./p/span/a/@title"))
    mydb.db_51job.remove()
    for item in all_div:
        info = {}
        info["position_name"] = item.xpath("./p/span/a/@title")[0]
        info["company_name"] = item.xpath("./span/a/@title")[0]
        info["address"] = item.xpath("./span[@class='t3']/text()")[0]
        salary = None
        try:
            salary = item.xpath("./span[@class='t4']/text()")[0]
        except:
            salary = ''
        info["salary_start"],info["salary_end"] = dealSalary(salary)
        info["date"] = item.xpath("./span[@class='t5']/text()")[0]
        info_list.append(info)
    mydb.db_51job.insert_many(info_list)

def searchDemo():
    res = mydb.db_51job.find({}).sort([("salary_start",1)])
    for item in res:
        print(item)

if __name__ == "__main__":
    demo()
    searchDemo()
    # print(dealSalary('2.5-2.8万'))