from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPolygonItem, QStyleOptionViewItem
from PyQt5.QtGui import QPolygon, QColor, QBrush, QIntValidator
from types import SimpleNamespace


class _VideoMarker(QGraphicsPolygonItem):
    def __init__(self, position, parent=None):
        self.position = position

        shape = QPolygon()
        shape.putPoints(0, 5, -2,-1, -2,0, 0,2, 2,0, 2,-1)

        self.setPolygon(shape)
        self.setPen(QPen(Qt.NoPen))
        self.setBush(QBrush(Qt.Blue))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)


class _Scene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._position = 0

        self._validator = QIntValidator()

        # items
        self._markers = list()

        line = self.addLine(QLineF(0, -50, 0, 50))
        line.setPen(QBrush(Qt.Red), 2)
        self._currLocator = line

        
        rect = self.addRect()

        self.backgroundBrush(Qt.lightGray)


    def mouseMoveEvent(self, event):
        QGraphicsScene.mouseMoveEvent(self, event)

        grabber = self.mouseGrabberItem()


class VideoProgressBar(QGraphicsView):
    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, n):
        self._position = n


    def reset(self, end, start=0):
        self._position = 0
        self._validator = QIntValidator(0, end)

        
    def addMarker(self, n):
        self._markers.append(VideoMarker())