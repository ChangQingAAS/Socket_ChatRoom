#!/usr/bin/python
# -*- coding: UTF-8 -*-
from socket import *

serverIP = '127.0.0.1'
serverPort = 10086

# 创建UDP套接字，使用IPv4协议
serverSocket = socket(AF_INET, SOCK_DGRAM) 
# 将UDP套接字绑定到指定端口
serverSocket.bind((serverIP,serverPort)) 
print("The server is ready to receive")

while True:
    # 接收数据
    data, addr = serverSocket.recvfrom(1024)

    # 输出来源
    print('Received from %s:%s.' % addr)

    # 获取收到的字符串
    print('Server received: %s' % data)

