from app.server.server_client import serverClient
from app.server.data_processor import dataProcessor
from threading import Thread, Lock
from app.Gui import tableGUI
from queue import Queue


class queueWithLock:
    def __init__(self, queueLength):
        self.queueLength = queueLength
        self.dataQueue = Queue(maxsize=queueLength)
        self.lock = Lock()


class MCUDevice:
    def __init__(self, serverIP, serverPort):
        dataProcessQueue = queueWithLock(30000)
        picDrawQueue = queueWithLock(30000)

        # 创建ServerClient实例
        serverClient1 = serverClient(serverIP, serverPort, dataProcessQueue)

        # 创建 DataProcessor 实例
        data_processor = dataProcessor(dataProcessQueue)

        # 创建一个线程来接受数据
        data_receive_thread = Thread(target=serverClient1.startServer)
        data_receive_thread.start()

        # 创建一个线程来处理文件
        data_process_thread = Thread(target=data_processor.processData)
        data_process_thread.start()

        # 创建一个线程来执行Gui
        gui_thread = Thread(target=tableGUI)
        gui_thread.start()

        data_receive_thread.join()
        data_process_thread.join()
        gui_thread.join()
