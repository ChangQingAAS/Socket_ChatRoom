import socket
import struct
import select
import threading
import time
import json
from common import packData, HEART_BEAT, NORMAL, HEADERSIZE, UPLOAD_FILE, DOWNLOAD_FILE, common_path
from download_files import download_file
from upload_files import upload_file

# 一些缓存
dataBuffer = {}
inputs = {}
outputs = {}

# 定义工作线程数量
workerThreadNum = 5

body = bytes()
# 我们需要一个缓存

# 用于存放用户conn及addr的字典
sock_list = {}


# 转发消息给每个用户
def send_msg_to_everyone(readdata, sock_in, sock_list):
    # print("have entered send_msg_to_everyone")
    if readdata:
        recv_dict = json.loads(readdata)
        user_name = recv_dict['user_name']
        send_message = recv_dict['send_message']
        addr = tuple(recv_dict['user_addr'])
        if send_message == '已上线':
            # 通知群内人员，谁进群了，遍历并发送给所有在聊天室的用户
            send_dict = {
                'user_name':
                user_name,
                'send_message':
                '我已进入聊天室\n' + '系统通知： 用户' + user_name + '进入聊天室\n' + '当前聊天室有' +
                str(len(sock_list)) + '人\n',
                'user_addr':
                str(addr),
                'user_login':
                True,
                'user_exit':
                False
            }
            # 将字典转换为JSON格式的字符串
            send_json = json.dumps(send_dict, ensure_ascii=False)
            for sock_c in sock_list.items():
                sock_c[1].send(packData(send_json.encode("utf-8"), NORMAL))

        elif send_message == 'EXIT':
            del sock_list[addr]
            try:
                sock_in.close()
                print("用户" + user_name + "离开聊天室")
                print('当前聊天室有' + str(len(sock_list)) + '人')
            except:
                pass
            # 通知群内人员，谁下线了，遍历并发送给所有在聊天室的用户
            send_dict = {
                'user_name':
                user_name,
                'send_message':
                '我已离开聊天室\n' + '系统通知： 用户' + user_name + '离开聊天室\n' + '当前聊天室有' +
                str(len(sock_list)) + '人\n',
                'user_addr':
                str(addr),
                'user_login':
                False,
                'user_exit':
                True
            }
            # 将字典转换为JSON格式的字符串
            send_json = json.dumps(send_dict, ensure_ascii=False)
            for sock_c in sock_list.items():
                sock_c[1].send(packData(send_json.encode("utf-8"), NORMAL))

        else:
            # 发送群聊消息 遍历并发送给所有在聊天室的用户
            send_dict = {
                'user_name': user_name,
                'send_message': send_message,
                'user_addr': str(addr),
                'user_login': True,
                'user_exit': False
            }
            # 将字典转换为JSON格式的字符串
            send_json = json.dumps(send_dict, ensure_ascii=False)
            for sock_c in sock_list.items():
                sock_c[1].send(packData(send_json.encode("utf-8"), NORMAL))

    else:
        # send_json = json.dumps(send_dict, ensure_ascii=False)
        # for sock_c in sock_list.items():
        #     sock_c[1].send(send_json.encode("utf-8"))
        del sock_list[addr]
        sock_in.close()


# 处理接收到的数据包
def dealData(sock_in, headPack, body, sock_list):
    # 用来调试代码
    # print("headPack: is " + str(headPack))

    readdata = body.decode("utf-8")
    print("接收消息：" + readdata)

    # 数据包类型为HEART_BEAT时
    if headPack[1] == HEART_BEAT:
        # recv_dict = json.loads(readdata)
        # user_name = recv_dict['user_name']
        sock_in.send(packData(b'Pong!', HEART_BEAT))
        # print("异常检测：已成功发出pong")
    # 数据包类型为NORMAL，即正常消息时
    elif headPack[1] == NORMAL:
        send_msg_to_everyone(readdata, sock_in, sock_list)
    # 上传文件
    elif headPack[1] == UPLOAD_FILE:
        upload_file(readdata)
    # 下载文件
    elif headPack[1] == DOWNLOAD_FILE:
        download_file(readdata)
    else:
        pass


# 工作线程, 负责一系列客户端的收发和数据处理
def workerThread(workerId):
    global HEADERSIZE
    # 当前监听的inputs和outputs均为空时, 原地等待
    while (len(inputs[workerId]) + len(outputs[workerId])) <= 0:
        # print(workerId,"<=0")
        time.sleep(0.5)

    while True:
        try:
            r_list, w_list, e_list = select.select(inputs[workerId],
                                                   outputs[workerId],
                                                   inputs[workerId], 100)
            for obj in r_list:
                try:
                    data = obj.recv(1024)
                except:
                    pass
                if data:
                    # 把数据存入缓冲区，类似于push数据
                    dataBuffer[obj] += data

                # 将该连接存到outputs里面等待select
                if obj not in outputs[workerId]:
                    outputs[workerId].append(obj)

            for obj in w_list:
                while len(dataBuffer[obj]) > HEADERSIZE:

                    headPack = struct.unpack('!3I',
                                             dataBuffer[obj][:HEADERSIZE])
                    bodySize = headPack[2]

                    if len(dataBuffer[obj]) < HEADERSIZE + bodySize:
                        print("数据包（%s Byte）不完整（总共%s Byte），继续接受 " %
                              (len(dataBuffer[obj]), HEADERSIZE + bodySize))
                        break
                    body = dataBuffer[obj][HEADERSIZE:HEADERSIZE + bodySize]

                    # 数据处理
                    dealData(obj, headPack, body, sock_list)

                    # 获取下一个数据包，类似于把数据pop出去
                    dataBuffer[obj] = dataBuffer[obj][HEADERSIZE + bodySize:]
                # 处理完后不再监听该socket 直到该socket再次发来数据
                outputs[workerId].remove(obj)
        except:
            pass


# 代码入口
def main():
    global dataBuffer
    global inputs
    global outputs
    # 预先启动workerThreadNum个工作线程
    for i in range(0, workerThreadNum):
        inputs[i] = []
        outputs[i] = []
        worker = threading.Thread(target=workerThread, args=(i, ))
        worker.start()

    serverIP = '127.0.0.1'
    serverPort = 10099
    # 创建TCP套接字，使用IPv4协议
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    # serverIP = socket.gethostname()

    # 将TCP套接字绑定到指定端口
    server.bind((serverIP, serverPort))
    # 等待客户端连接，最大连接数为5
    server.listen(5)
    print("The server is ready to receive")

    index = 0
    while True:
        conn, client_addr = server.accept()
        conn.setblocking(False)

        sock_list[client_addr] = conn
        # print("当前连接到的client_addr is", client_addr)

        print('当前聊天室有' + str(len(sock_list)) + '人')
        inputs[index % workerThreadNum].append(conn)
        dataBuffer[conn] = bytes()

        print('Accept new connection from %s:%s' % client_addr)
        index = index + 1

    server.close()


if __name__ == '__main__':
    main()
