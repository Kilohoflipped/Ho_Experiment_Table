from PyQt6.QtCore import QObject, pyqtSignal


class QtSignalBus(QObject):  # Qt信号的总线
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.QtSignalStream = {}  # 使用字典存储

    def addSignal(self, signalIdentifier, signalArgtype, signalSlot=None):
        newSignal = pyqtSignal(signalArgtype)
        if signalSlot:
            newSignal.connect(signalSlot)
        self.QtSignalStream[signalIdentifier] = newSignal
