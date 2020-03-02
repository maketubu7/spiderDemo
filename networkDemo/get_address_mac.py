# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 16:27
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : get_address_mac.py
# @Software: PyCharm
import psutil

if __name__ == '__main__':
    ###AddressFamily.AF_LINK标识的是mac地址
    ###AddressFamily.AF_INET标识的是IPV4地址
    ###AddressFamily.AF_INET6标识的是IPV6地址
    info = psutil.net_if_addrs()
    for k,v in info.items():
        print(k,v)
    mac = info['WLAN 3'][0].address  ###mac地址 无线网卡的第一个元素的address
    print(mac)