from PyQt5.QtWidgets import QGraphicsEllipseItem, QAbstractItemDelegate, QGraphicsItem
from PyQt5.QtCore import Qt, QPersistentModelIndex, QVariant, QPointF, pyqtSignal
from PyQt5.QtGui import QBrush



class JointGraphicsItem(QGraphicsEllipseItem):
    posChanged = pyqtSignal(QGraphicsItem, int, int)


    def __init__(self, index, x, y):
        super().__init__(x, y, 10, 10)
        self._index = index
        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))


    @property
    def index(self):
        return self._index


    def mouseMoveEvent(self, event):
        self.posChanged.emit(self, event.x(), event.y())
        self.setPos(event.pos())


    def mousePressEvent(self, event):
        pass