import os
import json
from common import common_path


def download_file(readdata):
    global common_path
    recv_dict = json.loads(readdata)
    user_name = recv_dict['user_name']
    file_path = recv_dict['send_message'].split(' ', 1)[1]
    file_name = file_path.split('/', 1)[1]
    try:
        common_path = os.path.abspath('').replace('\\', '/') + '/'
        print(common_path)
    except Exception as e:
        print(e)
    try:
        with open(common_path + "server_file/user/" + file_path,
                  "r",
                  encoding='utf-8',
                  errors='ignore') as server_file:
            if not os.path.exists(common_path + "client_file/" + user_name):
                os.makedirs(common_path + "client_file/" + user_name)
            with open(common_path + "client_file/" + user_name + "/" +
                      file_name,
                      "w+",
                      encoding='utf-8',
                      errors='ignore') as client_file:
                client_file.write(server_file.read())
                client_file.close()
            server_file.close()
        print("Have finished downloading.")
    except Exception as e:
        print("下载文件失败\n原因为：")
        print(e)
