from app.server.server_client import serverClient
from app.server.data_processor import dataProcessor
from queue import Queue
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QMutex


class QueueWithLock:
    def __init__(self, queueLength):
        self.queueLength = queueLength
        self.dataQueue = Queue(maxsize=queueLength)
        self.mutex = QMutex()


class MCUState:
    def __init__(self):
        self.rms = None
        self.period = None
        self.frequency = None
        self.samplingRate = None
        self.workState = None
        self.group = None
        self.index = None
        self.fig = None


class ServerClientThread(QThread):
    def __init__(self, serverIP, serverPort, dataProcessQueue, parent=None):
        super().__init__(parent=parent)
        self.serverClientInstance = serverClient(serverIP, serverPort, dataProcessQueue)

    def run(self):
        self.serverClientInstance.startServer()


class DataProcessorThread(QThread):
    def __init__(self, dataProcessQueue, AppQtSignalBus, parent=None):
        super().__init__(parent=parent)
        self.dataProcessorInstance = dataProcessor(dataProcessQueue, AppQtSignalBus)

    def run(self):
        self.dataProcessorInstance.processData()


class MCUDevice:
    def __init__(self, serverIP, serverPort, AppQtSignalBus):
        self.AppQtSignalBus = AppQtSignalBus  # Qt信号总线
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
        self.dataProcessorThreadInstance = DataProcessorThread(self.dataProcessQueue, self.AppQtSignalBus)
        self.dataProcessorThreadInstance.start()
