# coding:utf-8
from PyQt6.QtCore import Qt, QEasingCurve
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import ScrollArea, SmoothScrollArea, ToolTipFilter, PixmapLabel

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class ScrollInterface(GalleryInterface):
    """ Scroll interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.scroll,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )

        w = ScrollArea()
        label = PixmapLabel(self)
        label.setPixmap(QPixmap("app/resource/images/chidanta2.jpg").scaled(
            775, 1229, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))

        w.horizontalScrollBar().setValue(0)
        w.setWidget(label)
        w.setFixedSize(780, 420)
        w.setObjectName('imageViewer')

        card = self.addExampleCard(
            self.tr('Smooth scroll area'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/scroll_area/demo.py',
        )
        card.card.installEventFilter(ToolTipFilter(card.card, showDelay=500))
        card.card.setToolTip(self.tr('Chitanda Eru is too hot 🥵'))
        card.card.setToolTipDuration(2000)