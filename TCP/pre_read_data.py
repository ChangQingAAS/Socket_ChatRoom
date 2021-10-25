import json


def read_user_data():
    # 读取用户账号相关数据
    with open('./user_information.json', 'r') as f:
        user_data = json.load(f)

    user_data_str = str(user_data)
    user_data_dict = json.loads(user_data_str.replace("'", "\""))
    # print(user_data_dict)
    # user_data_tuple = user_data_dict.items()
    # for user_info in user_data_tuple:
    #     user_name_list.append(user_info[0])
    #     user_name = user_info[1]['user_name']
    #     user_password = user_info[1]['user_password']
    #     user_serverIP = user_info[1]["user_serverIP"]
    #     user_serverPort = user_info[1]["user_serverPort"]
    return user_data_dict
