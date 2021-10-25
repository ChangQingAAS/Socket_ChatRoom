import socket
import time
import json
import threading
import os
import struct
from pre_read_data import read_user_data
from common import packData, HEART_BEAT, NORMAL, HEADERSIZE, UPLOAD_FILE, DOWNLOAD_FILE, common_path
from login import user_login
from quit import QUIT

user_data_dict = {}
user_name = ''

# 我们需要一个缓存
dataBuffer = bytes()
# 未收到回应的心跳包计数
heartBeatCount = 0
heartBeatThread = 1
recvThread = 1
sendThread = 1


def write_log(user_name, send_message):
    '''
    在这里添加保存聊天数据的功能，和文件,暂时写在这里，可能以后会重构出去
    把这里改成json文件，用户名，信息，时间，ip地址，“能获得地点吗？”
    可根据用户名等信息查询过去的聊天记录（def query?)
    '''
    localtime = time.asctime(time.localtime(time.time()))
    with open("./message.txt", 'a+') as f:
        f.write("\n{\n")
        f.write("   user_name: " + user_name + "\n")
        f.write("   message: " + send_message + "\n")
        f.write("   time: " + localtime + "\n}")


# 在聊天室内发消息
def send_msg(sock, addr, user_name):
    # 等待1s 防止收发堆叠
    time.sleep(1)

    while True:
        # 等待1s 防止收发堆叠
        time.sleep(1)
        send_message = input("")
        send_dict = {'user_name': user_name, 'send_message': send_message}
        # 将字典转换为JSON格式的字符串
        send_json = json.dumps(send_dict, ensure_ascii=False)
        data = send_json.encode("utf-8")
        if send_message[0:6] == 'upload':
            sock.send(packData(data, UPLOAD_FILE))
            # print("have send file")
        elif send_message[0:8] == 'download':
            sock.send(packData(data, DOWNLOAD_FILE))
        else:
            sock.send(packData(data, NORMAL))
        # 日志，记录聊天记录
        write_log(user_name, send_message)
        if send_message == 'EXIT':
            QUIT()
            try:
                heartBeatThread.stop()
                sendThread.stop()
                recvThread.stop()
                sock.close()
                return 0
            except:
                return 0


# 心跳包线程:
def sendHeartBeat(client):
    global heartBeatCount
    while True:
        # print("异常检测：客户端发送心跳包, Ping!")
        client.send(packData(b'ping!', HEART_BEAT))
        heartBeatCount = heartBeatCount + 1
        if heartBeatCount > 3:
            # 后续处理
            print("ERROR: 心跳检测发现问题")

        time.sleep(30)


# 处理接收到的数据包
def dealData(sock, headPack, body, user_name):
    global heartBeatCount
    # 数据包类型为HEART_BEAT时
    if headPack[1] == HEART_BEAT:
        # print("客户端收到服务端返回心跳包, Pong!")
        heartBeatCount = heartBeatCount - 1
        # print("client 已成功发消息")
    elif headPack[1] == NORMAL:
        try:
            readdata = body.decode('utf-8')
            # print("readdata is " + readdata)
            recv_dict = json.loads(readdata)
            recv_user_name = recv_dict['user_name']
            recv_user_addr = recv_dict['user_addr']
            send_message = recv_dict['send_message']

            if recv_user_name != user_name:
                print('用户' + recv_user_name + ': ' + send_message)
        except Exception as e:
            print(e)
        # 等待1s 防止收发堆叠
        time.sleep(1)
    else:
        pass


# 接受聊天室内的消息，并打印
def recv_msg(sock, user_name):

    # 先发送上线通知
    send_message = '已上线'
    send_dict = {'user_name': user_name, 'send_message': send_message}
    # 将字典转换为JSON格式的字符串
    send_json = json.dumps(send_dict, ensure_ascii=False)
    data = send_json.encode("utf-8")
    sock.send(packData(data, NORMAL))
    # 等待1s 防止收发堆叠
    time.sleep(1)

    global dataBuffer

    while True:
        data = sock.recv(1024)
        if data:
            # 把数据存入缓冲区，类似于push数据
            dataBuffer += data

        while len(dataBuffer) > HEADERSIZE:
            headPack = struct.unpack('!3I', dataBuffer[:HEADERSIZE])
            # print("headPack is ", headPack)
            bodySize = headPack[2]

            if len(dataBuffer) < HEADERSIZE + bodySize:
                # print("数据包（%s Byte）不完整（总共%s Byte），继续接受 " % (len(dataBuffer), HEADERSIZE + bodySize))
                # print("len(dataBuffer) is ", len(dataBuffer))
                # print("bodySize is ", bodySize)
                break

            body = dataBuffer[HEADERSIZE:HEADERSIZE + bodySize]

            # 数据处理
            dealData(sock, headPack, body, user_name)

            # 获取下一个数据包，类似于把数据pop出去
            dataBuffer = dataBuffer[HEADERSIZE + bodySize:]


def chat(user_name):

    # 创建TCP套接字，使用IPv4协议
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    # serverIP = socket.gethostname()

    # 服务器的主机名和端口号
    serverIP = '192.168.182.1'
    serverPort = 10010
    server = (serverIP, serverPort)
    s.connect((serverIP, serverPort))

    global heartBeatThread
    global recvThread
    global sendThread

    heartBeatThread = threading.Thread(target=sendHeartBeat,
                                       name='heartBeatThread',
                                       args=(s, ))
    # tr = threading.Thread(target=recv_msg, args=(s, user_name), daemon=True)
    recvThread = threading.Thread(target=recv_msg, args=(s, user_name))
    sendThread = threading.Thread(target=send_msg, args=(s, server, user_name))

    recvThread.start()
    sendThread.start()
    heartBeatThread.start()

    recvThread.join()
    sendThread.join()
    heartBeatThread.join()

    time.sleep(1)

    # 关闭socket
    s.close()


def main():
    while True:
        global user_name, user_data_dict
        login_status, user_name = user_login()
        if login_status:

            chat(user_name)
            return 0
        else:
            QUIT()
    return 0


if __name__ == "__main__":
    user_data_dict = read_user_data()
    main()
