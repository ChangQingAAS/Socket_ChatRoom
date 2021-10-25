import json
from pre_read_data import read_user_data

user_data_dict = {}


def register_new_user(user_name, current_user_info_dict):
    user_data_dict[user_name] = current_user_info_dict

    json_str = json.dumps(user_data_dict, indent=4)
    with open('./user_information.json', 'w') as json_file:
        json_file.write(json_str)


def user_login():
    global user_data_dict
    # 读入用户数据
    user_data_dict = read_user_data()

    user_name = input('请输入您的用户名(按q退出)：')
    if user_name == 'q':
        return False
    # 如果该程序存在该用户则让其进入聊天室：
    elif user_name in user_data_dict.keys():
        user_password = input("请输入您的账户密码(您仅有两次机会)：")
        if user_password == user_data_dict[user_name]["user_password"]:
            print("您已登录您的账号。")
            print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----\n")
            print('-----------------%s------------------\n' % user_name)
            return (True, user_name)
        else:
            user_password = input("您的密码错误，请重新输入密码(这是最后一次机会！)：")
            if user_password == user_data_dict[user_name]["user_password"]:
                print("您已登录您的账号。")
                print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----\n")
                print('-----------------%s------------------\n' % user_name)
                return (True, user_name)
            else:
                return (False, user_name)

    else:
        choice = input("该账号不存在,请选择是否创建新的账号(Y or N)：")
        if choice == 'Y' or choice == 'y':
            user_name = input('请输入您想创建的用户名(按q退出)：')
            if user_name == 'q':
                return (False, user_name)
            elif user_name in user_data_dict.keys():
                user_name = input("您输入的账户名已存在，请重新输入您创建的账户名(按q退出)")
                if user_name == 'q':
                    return (False, user_name)
                if user_name not in user_data_dict.keys():
                    user_password = input("请输入该用户的密码：")
                    # user_serverIP = input("请输入连接的服务器的IP地址：")
                    user_serverIP = '127.0.0.1'
                    user_serverPort = 10015
                    new_user_dict = {
                        "user_name": user_name,
                        "user_password": user_password,
                        "user_serverIP": user_serverIP,
                        "user_serverPort": int(user_serverPort)
                    }
                    register_new_user(user_name, new_user_dict)
                    print("您已注册并登录该账号")
                    print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----\n")
                    print('-----------------%s------------------\n' %
                          user_name)
                    return (True, user_name)
            else:
                user_password = input("请输入您的账户密码：")
                # user_serverIP = input("请输入连接的服务器的IP地址：")
                user_serverIP = '127.0.0.1'
                user_serverPort = 10015
                new_user_dict = {
                    "user_name": user_name,
                    "user_password": user_password,
                    "user_serverIP": user_serverIP,
                    "user_serverPort": int(user_serverPort)
                }
                register_new_user(user_name, new_user_dict)
                print("您已注册并登录该账号")
                print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----\n")
                print('-----------------%s------------------\n' % user_name)
                return (True, user_name)
        elif choice == 'N' or choice == 'n':
            return (False, user_name)
