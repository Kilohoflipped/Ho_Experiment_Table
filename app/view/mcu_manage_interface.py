from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon

from app.components.mcu_card import MCUCardView
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView


class MCUManageInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.view.setObjectName('view')
        self.vBoxLayout = QVBoxLayout(self.view)  # 新增view组件的布局对象

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

        MCUCardViewGroup1.addMCUcard(
            workState=0,
            group=1,
            index=1,
            ratedCurrent=4,
            ratedFreq=1)

        self.vBoxLayout.addWidget(MCUCardViewGroup1)
