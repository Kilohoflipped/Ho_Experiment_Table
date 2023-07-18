# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QBrush, QColor, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QBasicTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import close
import pyqtgraph as pg

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, isDarkTheme
from app.common.QtSignalBus import QtAppSignalBus
from app.common.signal_bus import signalBus
from app.common.config import cfg
from app.server.MCUStateDict import MCUStateDict


class MCUCard(QFrame):
    """ MCU Card """

    def __init__(self, workState, group, index, ratedCurrent, ratedFreq, parent=None):
        """ workState: 0:OffLine  1:Online  2:Suspected malfunction """
        super().__init__(parent=parent)

        # 保存组别、编号、工作状态信息
        self.group = group
        self.index = index
        self.ratedCurrent = ratedCurrent
        self.ratedFreq = ratedFreq
        self.workState = workState

        # 连接Label更新信号与槽函数
        # if str(self.index) in QtAppSignalBus.QtSignalStream['MCUSignals']:  # 如果总线上存在对应编号的信号
        #     # 连接信号和槽函数
        #     QtAppSignalBus.getSignal(str(self.index), 'MCUSignals').connect(self.uptateCardWithSignal)

        # 创建所有View组件
        self.view = QWidget(parent=self)
        self.view.iconView = QWidget(parent=self.view)
        self.view.viewLeft = QWidget(parent=self.view)
        self.view.viewRight = QWidget(parent=self.view)
        self.view.viewGraph = QWidget(parent=self.view)
        self.view.viewLeft.setObjectName('MCUViewLeft')
        self.view.viewLeft.viewLeftTop = QWidget(parent=self.view.viewLeft)
        self.view.viewLeft.viewLeftBottom = QWidget(parent=self.view.viewLeft)

        # 创建布局
        self.view.hBoxLayout = QHBoxLayout(self)  # 整体布局
        self.view.hBoxLayout.setSpacing(0)

        self.view.iconView.hBoxLayout = QHBoxLayout(self.view.iconView)  # 图标布局
        self.view.hBoxLayout.addWidget(self.view.iconView)  # 将图标布局添加至整体布局中

        self.view.viewLeft.vBoxLayout = QVBoxLayout(self.view.viewLeft)  # 左侧布局,包括颜色小球,编号,额定值
        self.view.viewLeft.vBoxLayout.setSpacing(0)
        self.view.hBoxLayout.addWidget(self.view.viewLeft)  # 将左侧布局添加至整体布局中

        self.view.viewLeft.viewLeftTop.hBoxLayout = QHBoxLayout(self.view.viewLeft.viewLeftTop)  # 左侧顶部布局，包括颜色小球，编号
        self.view.viewLeft.vBoxLayout.addWidget(self.view.viewLeft.viewLeftTop)  # 将左侧顶部组件添加至左侧布局中

        self.view.viewLeft.viewLeftBottom.hBoxLayout = QHBoxLayout(self.view.viewLeft.viewLeftBottom)  # 左侧底部布局，包括额定值
        self.view.viewLeft.vBoxLayout.addWidget(self.view.viewLeft.viewLeftBottom)  # 将左侧底部组件添加至左侧布局中

        self.view.viewRight.vBoxLayout = QVBoxLayout(self.view.viewRight)
        self.view.hBoxLayout.addWidget(self.view.viewRight)  # 将右侧布局添加至整体布局中

        self.view.viewGraph.vBoxLayout = QVBoxLayout(self.view.viewGraph)
        self.view.hBoxLayout.addWidget(self.view.viewGraph)  # 将图表布局添加至整体布局中

        # 图标
        iconSize = 100
        scaledK = 10
        colorRed = QColor(255, 74, 0)
        self.iconLabel = QLabel(parent=self)
        self.iconLabel.setObjectName('iconLabel')
        self.iconLabel.svgRenderer = QSvgRenderer("app/resource/images/icons"
                                                  "/Mcu_card_icon_navigation_toolbar_top.svg")  # 读取图标svg
        self.iconLabel.iconPixmap = QPixmap(iconSize * scaledK, iconSize * scaledK)  # 创建渲染画布
        self.iconLabel.iconPixmap.setDevicePixelRatio(scaledK)
        self.iconLabel.iconPixmap.fill(QColor(0, 0, 0, 0))  # 填充透明像素
        self.iconLabel.painter = QPainter(self.iconLabel.iconPixmap)  # 新建画笔
        self.iconLabel.svgRenderer.render(self.iconLabel.painter, QRectF(0, 0, iconSize, iconSize))  # 绘制svg
        self.iconLabel.painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)  # 设置画笔混合模式为叠加
        self.iconLabel.painter.fillRect(QRectF(0, 0, iconSize, iconSize), colorRed)  # 绘制矩形以更改图标颜色
        self.iconLabel.painter.end()  # 结束绘制
        self.iconLabel.iconPixmap.scaled(iconSize, iconSize)  # 缩放大小
        self.iconLabel.setPixmap(self.iconLabel.iconPixmap)  # 显示图像
        self.view.iconView.hBoxLayout.addWidget(self.iconLabel)

        colorBallSize = 20
        self.colorLabel = QLabel(parent=self)
        self.colorLabel.setFixedSize(colorBallSize, colorBallSize)
        self.colorLabel.setObjectName('colorLabel')
        self.colorLabel.setPixmap(QPixmap(colorBallSize, colorBallSize))
        self.view.viewLeft.viewLeftTop.hBoxLayout.addWidget(self.colorLabel)

        self.groupIDLabel = QLabel("G{}-{}".format(self.group, self.index), parent=self)  # 组别-编号
        self.groupIDLabel.setObjectName('groupIDLabel')
        self.view.viewLeft.viewLeftTop.hBoxLayout.addWidget(self.groupIDLabel)

        self.ratedNumberLabel = QLabel("额定{}A-{}Hz".format(self.ratedCurrent, self.ratedFreq), parent=self)
        self.view.viewLeft.viewLeftBottom.hBoxLayout.addWidget(self.ratedNumberLabel)

        self.voltageLabel = QLabel("当前有效值:{}V".format(0), parent=self)
        self.view.viewRight.vBoxLayout.addWidget(self.voltageLabel)
        self.freqLabel = QLabel("当前频率:{}Hz".format(0), parent=self)
        self.view.viewRight.vBoxLayout.addWidget(self.freqLabel)

        self.graphCanvas = FigureCanvas(Figure())  # 创建空画布
        # self.ax = self.graphCanvas.add_subplot(111)
        graphPixmap = QPixmap(self.graphCanvas.size())
        self.graphCanvas.render(graphPixmap)
        self.graphLabel = QLabel(parent=self)
        self.graphLabel.setPixmap(graphPixmap)
        self.view.viewGraph.vBoxLayout.addWidget(self.graphLabel)

        #  设置定时事件
        self.timer = QBasicTimer()
        self.timer.start(500, self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId() and self.index in MCUStateDict.keys():
            self.voltageLabel.setText("当前有效值:{:.2f}V".format(MCUStateDict[self.index]['rms']))
            self.freqLabel.setText("当前频率:{:.2f}Hz".format(MCUStateDict[self.index]['frequency']))
            self.graphCanvas = FigureCanvas(MCUStateDict[self.index]['fig'])
            graphPixmap = QPixmap(self.graphCanvas.size())
            self.graphCanvas.render(graphPixmap)
            self.graphLabel.setPixmap(graphPixmap)
            close(MCUStateDict[self.index]['fig'])
            # self.graphCanvas.draw()


class MCUCardView(QWidget):
    """ MCU Card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)

        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()
        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.groupIDLabel = QLabel(title, self)
        self.vBoxLayout.addWidget(self.groupIDLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)
        self.groupIDLabel.setObjectName('MCUGroupObjectName')
        self.__setQss()

    def addMCUCard(self, workState, group, index, ratedCurrent, ratedFreq, parent=None):
        newMCUCard = MCUCard(workState, group, index, ratedCurrent, ratedFreq, parent=self)
        self.flowLayout.addWidget(newMCUCard)

    def __setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{theme}/mcu_card.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
