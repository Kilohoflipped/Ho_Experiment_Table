# Form implementation generated from reading ui file 'dataDisplayCard.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dataDisplayCard(object):
    def setupUi(self, dataDisplayCard):
        dataDisplayCard.setObjectName("dataDisplayCard")
        dataDisplayCard.resize(800, 400)
        self.deviceDataPlotWidget = QtWidgets.QWidget(parent=dataDisplayCard)
        self.deviceDataPlotWidget.setGeometry(QtCore.QRect(350, 50, 400, 300))
        self.deviceDataPlotWidget.setObjectName("deviceDataPlotWidget")
        self.deviceIDLabel = QtWidgets.QLabel(parent=dataDisplayCard)
        self.deviceIDLabel.setGeometry(QtCore.QRect(130, 50, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.deviceIDLabel.setFont(font)
        self.deviceIDLabel.setStyleSheet("border: 1px solid rgb(234, 234, 234);\n"
"border-radius: 10px;\n"
"background-color: rgb(253, 253, 253);")
        self.deviceIDLabel.setFrameShape(QtWidgets.QFrame.Shape.WinPanel)
        self.deviceIDLabel.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.deviceIDLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.deviceIDLabel.setObjectName("deviceIDLabel")

        self.retranslateUi(dataDisplayCard)
        QtCore.QMetaObject.connectSlotsByName(dataDisplayCard)

    def retranslateUi(self, dataDisplayCard):
        _translate = QtCore.QCoreApplication.translate
        dataDisplayCard.setWindowTitle(_translate("dataDisplayCard", "Form"))
        self.deviceIDLabel.setText(_translate("dataDisplayCard", "\"设备编号:{}\".format(a)"))