# -*- coding: utf-8 -*-
# @Time    : 2020/2/26 12:23
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : 51jobDemo.py
# @Software: PyCharm
import requests,json
from lxml import etree

##搜索职位的入口url
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

def demo():
    response = requests.get(url=url,headers=header)
    response.encoding = 'gbk'
    # print(response.text)
    html_51 = etree.HTML(response.text)
    all_div = html_51.xpath("//div[@id='resultList']//div[@class='el']")
    info_list = []
    # print(all_div[1].xpath("./p/span/a/@title"))
    for item in all_div:
        info = {}
        info["position_name"] = item.xpath("./p/span/a/@title")[0]
        info["company_name"] = item.xpath("./span/a/@title")[0]
        info["address"] = item.xpath("./span[@class='t3']/text()")[0]
        info["salary"] = item.xpath("./span[@class='t4']/text()")[0]
        info["date"] = item.xpath("./span[@class='t5']/text()")[0]
        info_list.append(info)
    print(json.dumps(info_list))

if __name__ == "__main__":
    demo()