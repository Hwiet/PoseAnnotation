from PyQt5.QtWidgets import QGraphicsEllipseItem, QAbstractItemDelegate
from PyQt5.QtCore import Qt, QPersistentModelIndex, QVariant, QPointF
from PyQt5.QtGui import QBrush



class JointItem(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))


    def mouseMoveEvent(self, event):
        self.setPos(event.pos())


    def mousePressEvent(self, event):
        pass