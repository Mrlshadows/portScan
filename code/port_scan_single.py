#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:Y4er

# 导入网络模块
import socket
# 导入解析命令行参数模块
import argparse
# 导入控制线程模块
import threading


def banner():
    print(r'''
 ____            _   ____                  
|  _ \ ___  _ __| |_/ ___|  ___ __ _ _ __  
| |_) / _ \| '__| __\___ \ / __/ _` | '_ \ 
|  __/ (_) | |  | |_ ___) | (_| (_| | | | |
|_|   \___/|_|   \__|____/ \___\__,_|_| |_|

Have fun. Author:Y4er''')

# 连接成功则端口打开，连接失败则端口关闭
def portscan(ip, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket()
        s.connect((ip, port))
        print('[+] {} is open.'.format(port))
        s.close()
    except:
        print('[-] {} is close.'.format(port))
    finally:
        pass

# 继承自Thread的MyThread类
class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, host, port, timeout):
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout

    def run(self):
        portscan(self.host, self.port, self.timeout)


if __name__ == '__main__':
    # 默认扫描端口号
    def_ports = [21, 22, 23, 25, 80, 110, 137, 138, 139, 443, 445, 873, 888, 1025, 1433, 1521, 2082, 2083, 2222, 3306,
                 3311, 3312, 3389, 4899, 5432, 5900, 6379, 7001, 7002, 7778, 8000, 8080, 8888, 11211, 27017, 43958,
                 50000, 65500]

    # 获取命令行参数
    parser = argparse.ArgumentParser(usage=banner())
    parser.add_argument('-a', help='target host', dest='host', required=True)
    parser.add_argument('-t', help='timeout', dest='timeout', type=int, required=True)
    parser.add_argument('-p', help='target port', dest='port', required=False)
    args = parser.parse_args()
    threads = []

    # 如果给定的检测端口号为范围
    if args.port:
        if '-' in args.port:
            limits = args.port.split('-')
            limits = list(map(int, limits))
            # 创建相应数量的线程
            for port in range(limits[0], limits[1] + 1):
                t = MyThread(args.host, port, args.timeout)
                threads.append(t)
    else:
        for port in def_ports:
            t = MyThread(args.host, port, args.timeout)
            threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()