#coding: utf-8
import time
import json
from socket import *
from locust import TaskSet, task, between, Locust, events, User
import struct

from common import packData, HEART_BEAT, NORMAL, HEADERSIZE


class SocketUser(User):
    # 目标地址
    host = '127.0.0.1'
    # 目标端口
    port = 10099
    # 等待时间, 用户连续的请求之间随机等待0.1~1s
    wait_time = between(0.1, 1)

    def __init__(self, *args, **kwargs):
        super(SocketUser, self).__init__(*args, **kwargs)
        self.client = socket(AF_INET, SOCK_STREAM)

    def on_start(self):
        self.client.connect((self.host, self.port))

    def on_stop(self):
        self.client.close()

    @task(100)
    def sendHeartBeat(self):
        start_time = time.time()
        try:
            #发送群聊消息 遍历并发送给所有在聊天室的用户
            send_dict = {
                'user_name': "admin",
                'send_message': 'Hello Server Are you OK?',
                'user_addr': '0.0.0.0',
                'user_login': True,
                'user_exit': False
            }
            # 将字典转换为JSON格式的字符串
            send_json = json.dumps(send_dict, ensure_ascii=False)
            self.client.send(packData(send_json.encode("utf-8"), NORMAL))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="Normal",
                                        name="SendMessage",
                                        response_time=total_time,
                                        response_length=0,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="Normal",
                                        name="SendMessage",
                                        response_time=total_time,
                                        response_length=0)

        start_time = time.time()
        try:
            data = self.client.recv(1024)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="Normal",
                                        name="RecvMessage",
                                        response_time=total_time,
                                        response_length=0,
                                        exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="Normal",
                                        name="RecvMessage",
                                        response_time=total_time,
                                        response_length=0)
