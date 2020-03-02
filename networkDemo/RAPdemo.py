# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 18:20
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : RAPdemo.py
# @Software: PyCharm
from scapy.all import srp,Ether,ARP,conf
from concurrent.futures import ThreadPoolExecutor

##设置不需要出现太多的信息，只解析mac地址就行
conf.verb = 0

#192.168.64.1-192.168.64.254
#192.168.64.0是网络地址
#192.168.64.255是广播地址

def hadle_arp_address(ip_address):
    ##srp，让arp数据包工作在数据帧，也就是数据链路层上，发数据帧
    ##ether工作在以太网，局域网中
    ##dst是目地广播mac地址，pdst是目的ip地址
    ##timeout是超时时间
    ##192.168.64.254  dns
    ##64-6E-69-F9-49-D91  mac
    ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout = 2)
    for snd, rcv in ans:
        ##80:05:88:7a:62:42 无线路由的mac地址
        print(rcv.sprintf(r"%Ether.src% & %ARP.psrc%"))  ##80:05:88:7a:62:42 & 92.168.64.254


t = ThreadPoolExecutor(10)
def get_other_mac():
    ##解析连接路由其他的设备的ip和mac地址
    t_list = []
    try:
        for ip in ip_list:
            thread = t.submit(hadle_arp_address,ip)
            t_list.append(thread)
        t.shutdown()
    except Exception as e:
        print(e)
        return
    finally:
        pass

ip_list = ["192.168.64."+str(_) for _ in range(1,255)]

if __name__ == '__main__':
    ###不需要出现太多的信息，只要解析到mac地址就行
    # hadle_arp_address("92.168.64.254")
    get_other_mac()