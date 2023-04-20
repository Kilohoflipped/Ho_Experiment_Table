from app.common.QtSignalBus import QtSignalBus
from PyQt6.QtCore import QThread
from app.Gui import tableGUI
from app.server.mcu_device import MCUDevice


class GUIThread(QThread):
    def __init__(self, AppQtSignalBus):
        super().__init__()
        self.AppQtSignalBus = AppQtSignalBus
        self.GUI = None

    def run(self):
        self.GUI = tableGUI()


class QtAppManager:
    def __init__(self):
        server_ip = "192.168.31.28"  # 设置服务器（PC）的IP地址
        server_port = 8888  # 设置服务器（PC）的端口
        self.AppQtSignalBus = QtSignalBus()  # 创建信号总线管理Qt信号

        # 创建一个线程来启动Gui
        self.GUIThreadInstance = GUIThread(self.AppQtSignalBus)
        self.GUIThreadInstance.start()

        # 创建一个MCU设备
        newMCUDevice = MCUDevice(server_ip, server_port, self.AppQtSignalBus)
