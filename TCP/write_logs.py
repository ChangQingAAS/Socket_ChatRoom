import time


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
        f.write("   time: " + localtime + "\n},")
