## 网络聊天室

基于TCP socket编程技术开发应用层协议，实现了一个naive的聊天室

### 基本功能 ：

- 服务端可以建立网络聊天室并等待客户端连接
- 客户端可以连入网络聊天室，并成功将自己的消息发送至服务端
- 多个客户端能及时收到并显示彼此的聊天消息
- 新用户加入和旧用户退出不会影响聊天室的正常运作
- 系统能正确处理粘包
- 使用心跳包进行异常断线检测和处理
  - 及时发现和处理客户端甚至服务端的异常掉线情况
  - 及时通知用户相关情况，保证系统的正常响应
- 系统进行了高并发的优化
  - 支持至少2000个用户的并发连接和并行聊天
- 系统支持文件传输功能
  - 做的很拉

### 系统设计：

#### 功能结构：

![image-20211025183538980](https://cdn.jsdelivr.net/gh/ChangQingAAS/for_picgo/img/20211025183540.png)

#### 工作流程：

- 服务端：

  ![image-20211025183642730](https://cdn.jsdelivr.net/gh/ChangQingAAS/for_picgo/img/20211025183642.png)



- 客户端：

  ![image-20211025183654195](https://cdn.jsdelivr.net/gh/ChangQingAAS/for_picgo/img/20211025183654.png)

