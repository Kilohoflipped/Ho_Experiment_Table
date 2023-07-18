from app.common.QtSignalBus import QtSignalBus
from PyQt6.QtCore import QThread
from app.Gui import tableGUI
from app.server.mcu_device import MCUDevice
from app.common.QtSignalBus import QtAppSignalBus
from app.server.data_processor import MCUState


class QtAppManager:
    def __init__(self):
        server_ip = "192.168.31.28"  # 设置服务器（PC）的IP地址
        server_port = 52134  # 设置服务器（PC）的端口
        self.QtAppSignalBus = QtAppSignalBus
        # 创建MCU设备管理器
        QtAppSignalBus.addSignalClass('MCUSignals')  # 新建信号种类
        self.MCUDeviceManager = MCUDeviceManager(server_ip, server_port)

        # 创建GUI
        self.GUI = tableGUI()  # PyQt中所有GUI操作都必须在主线程中进行


class MCUDeviceManager:
    def __init__(self, server_ip, server_port):
        # 创建一个MCU设备列表
        self.MCUDeviceList = []
        self.QtAppSignalBus = QtAppSignalBus
        for MCUDeviceIndex in range(10):  # 添加MCU设备
            self.MCUDeviceList.append(MCUDevice(server_ip, server_port))  # 向设备列表末尾追加
            QtAppSignalBus.addSignal(str(MCUDeviceIndex), 'MCUSignals', MCUState, signalSlot=None)
            server_port = server_port + 1
            # 每一个MCU设备添加一个PyQt信号，对应一个MCUCardView里面的MCUCard，连接在Card定义处通过总线进行
            # str(MCUDeviceIndex)
