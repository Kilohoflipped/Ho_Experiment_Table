from PyQt6.QtCore import QObject, pyqtSignal


class QtSignalBus(QObject):  # Qt信号的总线
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.QtSignalStream = {}  # 使用字典存储信号类别

    def addSignalClass(self, signalClassIdentifier):
        self.QtSignalStream[signalClassIdentifier] = {}  # 创建一个信号类别的字典

    def addSignal(self, signalIdentifier, signalClassIdentifier, signalArgtype, signalSlot=None):
        newSignal = pyqtSignal(signalArgtype)  # 创建一个新的信号
        setattr(self, f"{signalClassIdentifier}-{signalIdentifier}", newSignal)
        if signalSlot:
            newSignal.connect(signalSlot)
        # 把信号作为总线的属性，名字为"{signalClassIdentifier}-{signalSubclassIdentifier}_{signalIdentifier}"
        self.QtSignalStream[signalClassIdentifier][signalIdentifier] = newSignal  # 把信号添加到对应的字典中

    def getSignal(self, signalIdentifier, signalClassIdentifier):
        return self.QtSignalStream[signalClassIdentifier][signalIdentifier]  # 返回对应的信号


QtAppSignalBus = QtSignalBus()
