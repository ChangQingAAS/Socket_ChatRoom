#!/usr/bin/python
# -*- coding: UTF-8 -*-
from socket import *
import time

serverIP = '127.0.0.1'
serverPort = 10086

# 创建UDP套接字，使用IPv4协议
s = socket(AF_INET, SOCK_DGRAM) 

# 发送数据
s.sendto("Hello".encode("utf-8"), (serverIP, serverPort))

# 关闭socket
s.close()

