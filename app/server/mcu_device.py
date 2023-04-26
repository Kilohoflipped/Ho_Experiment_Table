from app.server.server_client import serverClient
from app.server.data_processor import dataProcessor
from queue import Queue
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex
from app.common.QtSignalBus import QtAppSignalBus


class QueueWithLock:
    def __init__(self, queueLength):
        self.queueLength = queueLength
        self.dataQueue = Queue(maxsize=queueLength)
        self.mutex = QMutex()


class ServerClientThread(QThread):
    def __init__(self, serverIP, serverPort, dataProcessQueue, parent=None):
        super().__init__(parent=parent)
        self.serverClientInstance = serverClient(serverIP, serverPort, dataProcessQueue)

    def run(self):
        self.serverClientInstance.startServer()


class DataProcessorThread(QThread):
    def __init__(self, dataProcessQueue, parent=None):
        super().__init__(parent=parent)
        self.dataProcessorInstance = dataProcessor(dataProcessQueue)

    def run(self):
        self.dataProcessorInstance.processData()


class MCUDevice:
    def __init__(self, serverIP, serverPort):
        self.dataProcessorThreadInstance = None
        self.serverClientThreadInstance = None
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.dataProcessQueue = QueueWithLock(10000)
        picDrawQueue = QueueWithLock(10000)
        self.ThreadsManager()

    def ThreadsManager(self):

        # 创建ServerClient 线程实例
        self.serverClientThreadInstance = ServerClientThread(self.serverIP, self.serverPort, self.dataProcessQueue)
        self.serverClientThreadInstance.start()

        # 创建 DataProcessor 线程实例
        self.dataProcessorThreadInstance = DataProcessorThread(self.dataProcessQueue)
        self.dataProcessorThreadInstance.start()
