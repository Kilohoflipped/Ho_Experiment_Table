from app.server.server_client import serverData
from app.server.data_processor import dataProcessor
from threading import Thread


class threadingManager:
    def __init__(self):
        server_ip = "192.168.31.28"  # 设置服务器（PC）的IP地址
        server_port = 8888  # 设置服务器（PC）的端口
        # serverData1 = serverData("192.168.31.28", 8888)
        # serverData1.startReceive()
        # 创建 DataProcessor 实例
        data_processor = dataProcessor()

        # 创建一个线程来处理文件
        file_path = 'app/server/data/data6.txt'
        data_process_thread = Thread(target=data_processor.dataProcess, args=(file_path,))
        data_process_thread.start()
        data_process_thread.join()
