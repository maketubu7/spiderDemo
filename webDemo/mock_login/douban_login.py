# -*- coding: utf-8 -*-
# @Time    : 2020/11/9 14:14
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : douban_login.py
# @Software: PyCharm
import requests, json, time
import numpy as np
import pickle, random
from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image
from io import BytesIO

# browser = webdriver.Chrome(executable_path=r'F:\spiderDemo\baseSpider\csdbSpider\chromedriver.exe')
browser = webdriver.Chrome(executable_path=r'F:\spiderDemo\baseSpider\chromedriver.exe')

login_url = 'https://accounts.douban.com/j/mobile/login/basic'
douban_url = 'https://www.douban.com/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
username = '18328577563'
password = 'dx818514'
header = {'User-Agent': user_agent}
post_data = {'name': username, 'password': password, 'ck': '', 'remember': 'true', 'ticket': '', 'randstr': '',
    'tc_app_id': ''}


def test_login():
    ## 获得请求得session的实例，在不断开连接的情况下可进行登录后访问
    session = requests.session()

    ## 用session进行访问
    response = session.post(login_url, headers=header, data=post_data)
    cookie = response.cookies.get_dict()
    ## 将cookie 写入到文件里，进行序列化访问
    with open('douban.cookie', 'wb') as f:
        pickle.dump(cookie, f)

    with open('douban.cookie', 'wb') as f:
        cookie = pickle.load(f)

    res = json.loads(response.text)

    ## 带着cookie去进行访问
    session.get(login_url)
    requests.get(login_url, cookies=cookie)


# 下载图片到本地
def get_image(img_url, imgname):
    # 以流的形式下载文件
    image = requests.get(img_url, stream=True)
    # str.join()方法用于将序列中的元素以指定的字符(str)连接生成一个新的字符串
    imgName = ''.join(["./", imgname, '.png'])
    with open(imgName, 'wb') as f:
        for chunk in image.iter_content(chunk_size=1024):  # 循环写入  chunk_size：每次下载的数据大小
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()

    return Image.open(imgName)


def compare_img(img, verify_img, dis=10, error=10):
    def compare_rgb(c1, c2):
        for i in range(3):
            if abs(c1[i] - c2[i]) > error:
                return 1
        return 0

    img_size = img.size
    for i in range(dis, img_size[0] - dis):
        for j in range(dis, img_size[1] - dis):
            c_img = img.load()[i, j]
            c_ver = verify_img.load()[i, j]
            if compare_rgb(c_img, c_ver):
                return i


# 采用物理加速度位移相关公式按照先快后慢的人工滑动规律进行轨迹计算，
# 同时还采用了模拟人滑动超过了缺口位置再滑回至缺口的情况以使轨迹更契合人工滑动轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = random.randint(2, 3) / 10
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move, 2))
    return track

def get_track_bk(distance):
    dis = int(distance / 2)
    return [dis]*2


def verify_login():
    cookie_dict = {}
    for item in browser.get_cookies():
        cookie_dict[item['name']] = item['value']
    res = requests.get(douban_url,headers=header,cookies=cookie_dict)
    text = res.text
    if u'马克图布' in text:
        return 1
    return 0


def selenium_login():
    browser.get(douban_url)
    browser.maximize_window()
    time.sleep(3)
    browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))
    phone_login = browser.find_element_by_xpath('//li[@class="account-tab-account"]')
    phone_login.click()
    time.sleep(1)
    user_ele = browser.find_element_by_xpath('//input[@id="username"]')
    pwd_ele = browser.find_element_by_xpath('//input[@id="password"]')
    user_ele.send_keys(username)
    pwd_ele.send_keys(password)

    submit_btn = browser.find_element_by_xpath('//a[@class="btn btn-account btn-active"]')
    submit_btn.click()
    time.sleep(2)
    if verify_login():
        print('登录成功')
        browser.close()
    else:
        code_login()
        if verify_login():
            print('登录成功')
            browser.close()
        else:
            print('登录失败')

def code_login():
    '''处理滑动验证码，保存图片截图'''
    time.sleep(3)
    browser.switch_to.frame(browser.find_element_by_id('tcaptcha_iframe'))

    image = browser.find_element_by_id('slideBg')
    verify_url = image.get_attribute('src')
    image_url = verify_url.replace('img_index=1', 'img_index=0')
    verify_img = get_image(verify_url, 'verify')
    img = get_image(image_url, 'image')

    ## 获取偏移量，即找到的位置减去滑块的开始位置
    x_move = compare_img(img, verify_img, error=50) * 0.4147 - 30
    action = ActionChains(browser)
    thumb = browser.find_element_by_id('tcaptcha_drag_thumb')
    action.click_and_hold(thumb).perform()
    tracks = get_track_bk(x_move)
    for i in tracks:
        action.move_by_offset(xoffset=i, yoffset=0).perform()
        action.reset_actions()
        time.sleep(2)
    action.release().perform()
    time.sleep(2)

if __name__ == "__main__":
    selenium_login()
