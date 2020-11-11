# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 9:44
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : aircode.py
# @Software: PyCharm
# @content : 爬取机场三字码 入口 https://airport.supfree.net/index.asp?page={}

import requests
from scrapy import Selector
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+pymysql://root:123456@localhost:3306/spider_demo')

urls = ['https://airport.supfree.net/index.asp?page={}'.format(_) for _ in range(1,284)]

def get_aircode(urls):
    res = []
    for url in urls:
        print(url)
        response = requests.get(url)
        response.encoding = 'gbk'
        html = response.text
        sel = Selector(text=html)
        all_tr = sel.xpath('//table//tr')
        for tr in all_tr[1:]:
            tmp = []
            city = tr.xpath('.//td[1]/span/text()').extract()[0]
            try:
                airport_name = ''
                airport_pinyin = ''
                three_code = ''
                city = tr.xpath('.//td[1]/span/text()').extract()[0]
                airport = tr.xpath('.//td[2]/text()').extract()
                if len(airport) == 1:
                    three_code = airport[0]
                airport = tr.xpath('.//td[4]/text()').extract()
                if len(airport) ==1:
                    airport_name = airport[0]
                airport = tr.xpath('.//td[5]/text()').extract()
                if len(airport) == 1:
                    airport_pinyin = airport[0]
                tmp.append(city)
                tmp.append(three_code)
                # tmp.append(four_code)
                tmp.append(airport_name)
                tmp.append(airport_pinyin)
                res.append(tmp)
            except:
                print(city)
                pass
    print(len(res))
    df = pd.DataFrame(res,columns=['city','code3','air_name','air_pinyin'])
    df.to_csv('airport_code.csv',index=None,encoding='utf-8')


if __name__ == "__main__":
    get_aircode(urls)
    # df = pd.read_csv(open(r'C:\Users\lenovo\Desktop\山西图谱\air_code.csv'),encoding='utf-8')
    # print(df.head())
    # df.to_sql('air_code',engine,if_exists='replace',index=False)




