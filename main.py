from app.server.mcu_device import MCUDevice
from queue import Queue

if __name__ == '__main__':
    server_ip = "192.168.31.28"  # 设置服务器（PC）的IP地址
    server_port = 8888  # 设置服务器（PC）的端口
    threadingManage = MCUDevice(server_ip, server_port)
