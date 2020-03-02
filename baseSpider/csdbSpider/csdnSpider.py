# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 17:22
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : csdnSpider.py
# @Software: PyCharm
import re,json,ast
from datetime import datetime

import requests
from urllib import parse
from selenium import webdriver
from scrapy import Selector
from ormDemo.models.models import *

domain = "https://bbs.csdn.net"
left_menu_js = 'https://bbs.csdn.net/dynamic_js/left_menu.js?csdn'
# browser = webdriver.Chrome(executable_path=r'F:\spiderDemo\baseSpider\csdbSpider\chromedriver.exe')
# browser.get(domain)
# cookies = browser.get_cookies()
# cookie_dict = {}
# for item in cookies:
#     cookie_dict[item["name"]] = item["value"]



def format_data(content):
    return content.replace('\t','').replace('\n','')

def get_detail_page_info(url):
    topic_id = url.split('/')[-1]
    res_text = requests.get(url).text
    sel = Selector(text=res_text)
    all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")
    topic_item = all_divs[0]
    ##标题
    content = sel.xpath("//div[@class='owner_top clearfix']/h3/span[1]/@title").extract()[0]
    ##点赞数
    praised_nums = topic_item.xpath(".//label[@class='red_praise digg']//em/text()").extract()[0]
    ##结贴率
    jtl_str = topic_item.xpath(".//div[@class='close_topic']/text()").extract()[0]
    jtl = 0
    jtl_match = re.search("(\d+)%", jtl_str)
    if jtl_match:
        jtl = int(jtl_match.group(1))
    return (content,praised_nums,jtl)


def get_node_json():
    left_menu_text = requests.get(url=left_menu_js).text
    node_search_match = re.search(r"forumNodes: (.*])",left_menu_text)
    if node_search_match:
        nodes = node_search_match.group(1).replace("null","None")
        nodes_json = ast.literal_eval(nodes)
        return nodes_json
    return []

def process_node_list(nodes_json,url_list):
    ##将js的格式提取url到list中
    for item in nodes_json:
        if "url" in item:
            if item["url"]:
                url_list.append(item["url"])
            else:
                pass
        if "children" in item:
            process_node_list(item["children"],url_list)

def get_last_url():
    url_list = []
    nodes_json = get_node_json()
    process_node_list(nodes_json,url_list)
    recommend_url = list(map(lambda x:parse.urljoin(domain,x+"/recommend"),url_list))
    closed_url = list(map(lambda x:parse.urljoin(domain,x+"/closed"),url_list))
    all_url = url_list + recommend_url + closed_url
    return all_url

topic_url_list = []

def del_topic(url):
    # url = 'https://bbs.csdn.net/forums/MobileAD/closed'
    response = requests.get(url=url)
    sel = Selector(text=response.text)
    all_trs = sel.xpath('//div[@class="forums_table_c"]/table/tbody/tr')
    content = sel.xpath("//div[@class='fl']/a[3]/text()").extract()[0]
    page_info = sel.xpath("//div[@class='page_nav']/em[1]/text()").extract()[0]
    for tr in all_trs:
        res = {}
        res["status"] = tr.xpath('./td[@class="forums_topic_flag"]/span/text()').extract()[0]
        res["score"] = tr.xpath('./td[@class="forums_score"]/em/text()').extract()[0]
        topic_urls = tr.xpath('./td[@class="forums_topic"]/a/@href').extract()
        if len(topic_urls) > 1:
            topic_url = parse.urljoin(domain,topic_urls[1])
        else:
            topic_url = parse.urljoin(domain, topic_urls[0])
        topic_url_list.append(topic_url)
        detail_page_info = get_detail_page_info(topic_url)
        res["content"] = detail_page_info[0]
        res["praised_nums"] = detail_page_info[1]
        res["jtl"] = detail_page_info[2]
        res['topic_url'] = topic_url
        res['topic_id'] = int(topic_url.split('/')[-1])
        res['topic_title'] = tr.xpath('./td[@class="forums_topic"]/a/text()').extract()[0].replace('【','').replace('】','')
        author_url = parse.urljoin(domain,tr.xpath('./td[@class="forums_author"]/a/@href').extract()[0])
        res['author_url'] = author_url
        res['author_id'] = author_url.split('/')[-1]
        res['auth_name'] = tr.xpath('./td[@class="forums_author"]/a/text()').extract()[0]
        view_num = tr.xpath('./td[@class="forums_reply"]/span/text()').extract()[0]
        create_date = tr.xpath('./td[@class="forums_author"]/em/text()').extract()[0]
        answer_last_date = tr.xpath('./td[@class="forums_last_pub"]/em/text()').extract()[0]
        res['create_date'] = datetime.strptime(create_date,"%Y-%m-%d %H:%M")
        res['last_pub_time'] = datetime.strptime(answer_last_date,"%Y-%m-%d %H:%M")
        res['answer_nums'] = int(view_num.split('/')[0])
        res['click_nums'] = int(view_num.split('/')[1])

        topic = Topic()
        topic.status = res.get("status")
        topic.title = res.get("topic_title")
        topic.topic_id = res.get("topic_id")
        topic.author = res.get("author_id")
        topic.click_nums = res.get("click_nums")
        topic.answer_nums = res.get("answer_nums")
        topic.create_time = res.get("create_date")
        topic.last_pub_time = res.get("last_pub_time")
        topic.score = res.get("score")
        topic.content = res.get("content")
        topic.praised_nums = res.get("praised_nums")
        topic.jtl = res.get("jtl")

        exists_topic = topic.select().where(Topic.topic_id == topic.topic_id)

        if exists_topic:
            topic.save()
        else:
            topic.save(force_insert=True)


def parse_topic(url):
    #获取帖子的详情以及回复
    topic_id = url.split("/")[-1]
    res_text = requests.get(url).text
    sel = Selector(text=res_text)
    all_divs = sel.xpath("//div[starts-with(@id, 'post-')]")

    for answer_item in all_divs[1:]:
        content = format_data(answer_item.xpath(".//div[@class='post_body post_body_min_h']/text()").extract()[0])

        if not content:
            continue
        answer = Answer()
        answer.topic_id = topic_id
        author_info = answer_item.xpath(".//div[@class='nick_name']//a[1]/@href").extract()[0]
        author_id = author_info.split("/")[-1]
        create_time = answer_item.xpath(".//label[@class='date_time']/text()").extract()[0]
        create_time = datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
        answer.author = author_id
        answer.create_time = create_time
        praised_nums = answer_item.xpath(".//label[@class='red_praise digg']//em/text()").extract()[0]
        answer.parised_nums = int(praised_nums)
        answer.content = content

        answer.save()

    # next_page = sel.xpath("//a[@class='pageliststy next_page']/@href").extract()
    # if next_page:
    #     next_url = parse.urljoin(domain, next_page[0])
    #     parse_topic(next_url)



def parse_author(url):
    author_id = url.split("/")[-1]
    # 获取用户的详情
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0',
    }
    res_text = requests.get(url, headers=headers).text
    sel = Selector(text=res_text)
    author = Author()
    author.id = author_id
    all_li_strs = sel.xpath("//ul[@class='mod_my_t clearfix']/li/span/text()").extract()
    click_nums = all_li_strs[0]
    original_nums = all_li_strs[1]
    forward_nums = int(all_li_strs[2])
    rate = int(all_li_strs[3])
    answer_nums = int(all_li_strs[4])
    parised_nums = int(all_li_strs[5])

    author.click_nums = click_nums
    author.original_nums = original_nums
    author.forward_nums = forward_nums
    author.rate = rate
    author.answer_nums = answer_nums
    author.parised_nums = parised_nums

    desc = sel.xpath("//dd[@class='user_desc']/text()").extract()
    if desc:
        author.desc = desc[0].strip()
    person_b = sel.xpath("//dd[@class='person_b']/ul/li")
    for item in person_b:
        item_text = "".join(item.extract())
        if "csdnc-m-add" in item_text:
            location = item.xpath(".//span/text()").extract()[0].strip()
            author.location = location
        else:
            industry = item.xpath(".//span/text()").extract()[0].strip()
            author.industry = industry
    name = sel.xpath("//h4[@class='username']/text()").extract()[0]
    author.name = name.strip()
    existed_author = Author.select().where(Author.id == author_id)
    if existed_author:
        author.save()
    else:
        author.save(force_insert=True)


if __name__ == "__main__":
    # urls = get_last_url()
    # print(len(urls))
    # print(urls[567])
    # print(requests.get('https://bbs.csdn.net/forums/MobileAD/closed').text)
    # parse_list('https://bbs.csdn.net/forums/WindowsMobile')
    # del_topic('https://bbs.csdn.net/forums/WindowsMobile?page=12')
    # all_page = re.match('共(\d+)页', str).group(1)
    # print(all_page)
    # topic_url_list = ['https://bbs.csdn.net/topics/390963960', 'https://bbs.csdn.net/topics/391823625']
    # print(topic_url_list)
    # for url in topic_url_list:
    #     parse_topic(url)
    parse_topic('https://bbs.csdn.net/topics/391897593')
