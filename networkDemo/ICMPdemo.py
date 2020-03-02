# -*- coding: utf-8 -*-
# @Time    : 2020/2/24 21:22
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : ICMPdemo.py
# @Software: PyCharm
from concurrent.futures import ThreadPoolExecutor
from scapy.all import sr, IP,ICMP,conf

conf.verb = 0
def hand_alive(ip):
    #srp是让ARP协议工作在数据链路层上，发送的时数据帧
    #sr是让ICMP协议工作在网络层伤，发送的时数据包
    ##ICMP协议不受网络范围的限制
    ##是私有的IP地址段，私有IP地址只在当前网络中可用，NAT协议进行映射的
    ##192.168.75.213是我的私有ip
    ##20.194.140.127是我的共有IP
    ##20.194.140.127公有IP，影射着很多私有的IP地址
    ##scapy来进行ICMP协议测试

    ans, unans = sr(IP(dst=ip)/ICMP(),retry=0,timeout=2)

    for snd, rcv in ans:
        print(rcv.sprintf(r"%IP.src% is alive"))

def many_executor():
    t = ThreadPoolExecutor(10)
    t_list = []
    ip_list = ["192.168.64."+str(_) for _ in range(1,255)]

    for ip in ip_list:
        thread = t.submit(hand_alive,ip)
        t_list.append(thread)
    t.shutdown()

if __name__ == "__main__":
    hand_alive('8.8.8.8')
    # many_executor()