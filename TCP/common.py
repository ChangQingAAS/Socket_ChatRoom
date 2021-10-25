import struct

# 通信双方需要知道包头的长度
HEADERSIZE = 12
HEART_BEAT = 0
NORMAL = 1
UPLOAD_FILE = 2
DOWNLOAD_FILE = 3
common_path = "C:/Users/admin/Desktop/必修课/计算机网络/socket编程实践/code/TCP/"


# 给数据打包，加上版本号 消息类型 包长度
# packetType=0 为心跳检测包
# packetType=1 为普通消息
# packetType=2 为请求上传文件
# packetType=3 为请求下载文件

def packData(data, packetType):
    # 定义数据包头部由版本号和包长三个4位无符号整数组成
    version = 1
    bodyLen = len(data)
    header = [version, packetType, bodyLen]
    # !代表网络字节顺序NBO（Network Byte Order），3I代表3个unsigned int数据
    headPack = struct.pack("!3I", *header)
    return headPack + data
