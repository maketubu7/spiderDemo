import requests
from multiprocessing import Queue
from lxml import etree
import threading,re
from baseSpider.mongoUtil import mongo_client
from baseSpider.data_consts import proxy
import traceback


#处理页码类
class Crawl_page(threading.Thread):
    #重写父类
    def __init__(self,thread_name,page_queue,data_queue):
        super(Crawl_page,self).__init__()
        #线程的名称
        self.thread_name = thread_name
        #页码的队列
        self.page_queue = page_queue
        #数据的队列
        self.data_queue = data_queue
        #默认请求头
        self.header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "search.51job.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36",
        }

    def run(self):
        print('当前启动的处理页码的任务为%s'%self.thread_name)
        # while True
        while not page_flag:
            #Queue队列去put或者get的时候，需要设置block
            #它默认为True，需要设置成flase
            #当前队列里没有数据了，将会抛出异常,empty,full
            try:
                #通过get方法，将里面的页码get出来,get为空的时候，抛异常
                page = self.page_queue.get(block=False)
                page_url = 'https://search.51job.com/list/000000,000000,0000,00,9,99,python,2,'+str(page)+'.html'
                print(page_url)
                #请求当前构造的url
                #设置代理,当前使用的是阿布云的动态代理,站大爷
                #此处我们加上了代理,requests方法请求
                response = requests.get(url=page_url,headers=self.header)
                #设置了网页编码
                response.encoding = 'gbk'
                #将我们请求回来的网页文本数据放到数据队列里面去
                self.data_queue.put(response.text)
            except Exception as e:
                return



#处理网页文本数据处理类
class Crawl_html(threading.Thread):
    #从页码解析过来的文本数据，需要保存到data_queue
    def __init__(self,thread_name,data_queue,lock):
        super(Crawl_html,self).__init__()
        self.thread_name = thread_name
        self.data_queue = data_queue
        self.lock = lock

    def run(self):
        print("当前启动处理文本任务的线程为%s"%self.thread_name)
        while not data_flag:
            try:
                #把文本数据get出来
                text = self.data_queue.get(block = False)
                #相应的方法进行处理
                # print(text)
                result = self.__parse(text)
                #锁这个概念
                print('result')
                with self.lock:
                    print("start insert ")
                    mongo_client.insert_data(result)
            except:
                pass


    def __dealSalary(self,salary_desc):
        if salary_desc:
            patterm = re.compile(r'\d+\.?\d*')
            res = patterm.findall(salary_desc)
            if len(res) == 1:
                return (0, 0)
            if len(res) > 1:
                res = sorted([float(i) for i in res])
                if '万' in salary_desc:
                    res = [int(i * 10000) for i in res]
                    return tuple(res)
                if 'k' in salary_desc.lower() or '千' in salary_desc:
                    res = [int(i * 1000) for i in res]
                    return tuple(res)
                return tuple([int(i) for i in res])
        else:
            return (0, 0)

    def __parse(self,text):
        html_51 = etree.HTML(text)
        all_div = html_51.xpath("//div[@id='resultList']//div[@class='el']")
        info_list = []
        # print(all_div[1].xpath("./p/span/a/@title"))
        # mydb.db_51job.remove()
        for item in all_div:
            info = {}
            info["position_name"] = item.xpath("./p/span/a/@title")[0]
            info["company_name"] = item.xpath("./span/a/@title")[0]
            info["address"] = item.xpath("./span[@class='t3']/text()")[0]
            try:
                salary = item.xpath("./span[@class='t4']/text()")[0]
            except Exception as e:
                salary = ''
            info["salary_start"], info["salary_end"] = self.__dealSalary(salary)
            info["date"] = item.xpath("./span[@class='t5']/text()")[0]
            # print(info)
            info_list.append(info)
        ##返回结果
        return info_list

#我们定义两个全局的flag
page_flag = False
data_flag = False

def main():
    #定义两个队列，存放页码的队列，存放文本数据的队列
    page_queue = Queue()
    data_queue = Queue()

    #定义一个锁
    lock = threading.Lock()


    #需要将页码放入到页码队列里面去
    for page in range(1,4):
        #通过put方法，把页码放到page_queue
        page_queue.put(page)

    #打印了一个提示信息,page_queue.qsize()返回当前队里的长度
    print('当前页码队列的总量为%s'%page_queue.qsize())

    #列表,包含了线程的名称,页码线程,开了三个线程
    crawl_page_list = ["页码处理线程1号","页码处理线程2号","页码处理线程3号"]
    page_thread_list = []
    for thread_name_page in crawl_page_list:
        thread_page = Crawl_page(thread_name_page,page_queue,data_queue)
        #启动线程
        thread_page.start()
        page_thread_list.append(thread_page)


    #设置三个线程，处理文本数据
    parseList = ["文本处理线程1号","文本处理线程2号","文本处理线程3号"]
    parse_thread_list = []
    for thread_name_parse in parseList:
        thread_parse = Crawl_html(thread_name_parse,data_queue,lock)
        thread_parse.start()
        parse_thread_list.append(thread_parse)

    #设置线程的推出机制
    global page_flag
    #在page_queue为空的时候,while就不成立
    while not page_queue.empty():
        pass
    page_flag = True

    #结束页码处理线程
    for thread_page_join in page_thread_list:
        thread_page_join.join()
        print(thread_page_join.thread_name,'处理结束')

    global data_flag
    while not data_queue.empty():
        print(1)
        pass
    data_flag = True

    for thread_parse_join in parse_thread_list:
        thread_parse_join.join()
        print(thread_parse_join.thread_name,"处理结束")


if __name__ == '__main__':
    #入口函数
    main()
