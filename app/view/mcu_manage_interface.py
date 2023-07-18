from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon

from app.components.mcu_card import MCUCardView
from app.view.gallery_interface import ToolBar
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView


class MCUManageInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.view.setObjectName('view')
        # self.toolBar = ToolBar('设备控制面板', 'MCU DeVice Manager', self)
        self.vBoxLayout = QVBoxLayout(self.view)  # 新增view组件的布局对象

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.__initWidget()
        self.__loadMCUS()

    def __initWidget(self):
        self.__setQSS()

    def __setQSS(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{theme}/home_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __loadMCUS(self):
        MCUCardViewGroup1 = MCUCardView(title=self.tr('Group 1'), parent=self.view)
        MCUCardViewGroup1.addMCUCard(
            workState=0,
            group=1,
            index=1,
            ratedCurrent=4,
            ratedFreq=1)
        MCUCardViewGroup1.addMCUCard(
            workState=0,
            group=1,
            index=2,
            ratedCurrent=4,
            ratedFreq=2)
        MCUCardViewGroup1.addMCUCard(
            workState=0,
            group=1,
            index=3,
            ratedCurrent=4,
            ratedFreq=3)
        MCUCardViewGroup1.addMCUCard(
            workState=0,
            group=1,
            index=4,
            ratedCurrent=4,
            ratedFreq=1)
        MCUCardViewGroup1.addMCUCard(
            workState=0,
            group=1,
            index=5,
            ratedCurrent=4,
            ratedFreq=0)

        MCUCardViewGroup2 = MCUCardView(title=self.tr('Group 2'), parent=self.view)
        MCUCardViewGroup2.addMCUCard(
            workState=0,
            group=2,
            index=6,
            ratedCurrent=6,
            ratedFreq=1)
        MCUCardViewGroup2.addMCUCard(
            workState=0,
            group=2,
            index=7,
            ratedCurrent=6,
            ratedFreq=2)
        MCUCardViewGroup2.addMCUCard(
            workState=0,
            group=2,
            index=8,
            ratedCurrent=6,
            ratedFreq=3)
        MCUCardViewGroup2.addMCUCard(
            workState=0,
            group=2,
            index=9,
            ratedCurrent=6,
            ratedFreq=1)
        MCUCardViewGroup2.addMCUCard(
            workState=0,
            group=2,
            index=10,
            ratedCurrent=6,
            ratedFreq=0)
        self.vBoxLayout.addWidget(MCUCardViewGroup1)
        self.vBoxLayout.addWidget(MCUCardViewGroup2)
