from app.server.server_client import serverClient
from app.server.data_processor import dataProcessor
from threading import Thread
from app.Gui import tableGUI


class threadingManager:
    def __init__(self):
        server_ip = "192.168.31.28"  # 设置服务器（PC）的IP地址
        server_port = 8888  # 设置服务器（PC）的端口
        # serverData1 = serverData("192.168.31.28", 8888)
        # serverData1.startServer()
        # 创建 DataProcessor 实例
        data_processor1 = dataProcessor()

        # 创建ServerClient实例
        serverClient1 = serverClient(server_ip,server_port)

        # 创建一个线程来接受数据
        data_receive_thread = Thread(target=serverClient1.startServer())
        data_receive_thread.start()
        data_receive_thread.join()

        # 创建一个线程来处理文件
        file_path = 'app/server/data/data6.txt'
        data_process_thread = Thread(target=data_processor1.dataProcess, args=(file_path,))
        data_process_thread.start()
        data_process_thread.join()

        # 创建一个线程来执行Gui
        gui_thread = Thread(target=tableGUI)
        gui_thread.start()
        gui_thread.join()
