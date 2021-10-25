import os
import json
from common import common_path


def upload_file(readdata):
    global common_path
    recv_dict = json.loads(readdata)
    user_name = recv_dict['user_name']
    file_name = recv_dict['send_message'].split(' ', 1)[1]
    # print("file_name is " + file_name)
    try:
        common_path = os.path.abspath('').replace('\\', '/') + '/'
        print(common_path)
    except Exception as e:
        print(e)
    try:
        if not os.path.exists(common_path + "server_file/user/" + user_name):
            os.makedirs(common_path + "server_file/user/" + user_name)
        with open(common_path + "server_file/user/" + user_name + "/" +
                  file_name,
                  "w+",
                  encoding='utf-8',
                  errors='ignore') as server_file:
            with open(common_path + "client_file/" + user_name + "/" +
                      file_name,
                      "r",
                      encoding='utf-8',
                      errors='ignore') as client_file:
                server_file.write(client_file.read())
                client_file.close()
            server_file.close()
        print("Have finished uploading.")
    except Exception as e:
        print("上传文件失败\n原因为：")
        print(e)
