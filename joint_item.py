from PyQt5.QtWidgets import QGraphicsEllipseItem, QAbstractItemDelegate, QGraphicsItem
from PyQt5.QtCore import Qt, QPersistentModelIndex, QVariant, QPointF, pyqtSignal, QRectF
from PyQt5.QtGui import QBrush



class JointGraphicsItem(QGraphicsEllipseItem):
    posChanged = pyqtSignal(QGraphicsItem, int, int)


    def __init__(self, index, point: QPointF):
        super().__init__(QRectF(point, point + QPointF(10, 10)))
        self._index = index
        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))

        self.setFlags(QGraphicsItem.ItemIsMovable)


    @property
    def index(self):
        return self._index