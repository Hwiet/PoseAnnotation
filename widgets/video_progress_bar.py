# QStyle - The QStyle class is an abstract base class that encapsulates the
# look and feel of a GUI (***platform-specific look***)
#    QStylePainter - The QStylePainter class is a convenience class for drawing
#    QStyle elements inside a widget (convenience version of QPainter)

# QStyleOptionSlider - The QStyleOptionSlider class is used to describe the
# parameters needed for drawing a slider.

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QMediaPlayer


class VideoProgressBar(QSlider):
    def __init__(self, parent=None):
        if parent is not None:
            super().__init__(parent)
        else:
            super().__init__()

        self.setOrientation(Qt.Horizontal)

    @pyqtSlot(int)
    def setRange(self, duration):
        super().setRange(0, duration)


class VideoProgressToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._widget = VideoProgressBar()

        self.addWidget(self._widget)
        self.setAllowedAreas(Qt.BottomToolBarArea)

    @property
    def widget(self):
        return self._widget