from functools import partial
from typing import Dict, List

from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QPointF,
    QLineF,
    QRectF
)

from PyQt5.QtWidgets import (
    QGraphicsObject,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsLineItem,
    QGraphicsSimpleTextItem
)

from PyQt5.QtGui import (
    QPen,
    QBrush,
    QFont,
    QTransform
)

class Grabber(QGraphicsRectItem):
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        self.parentItem().setPos(event.pos())

    def mouseReleaseEvent(self, event):
        self.parentItem().submitPos(event.pos(), 0)

class JointItem(QGraphicsObject):
    LABEL_OFFSET = QPointF(12, -3)
    POINT_WIDTH = 7

    positionChanged = pyqtSignal(QGraphicsItem, QPointF)

    def __init__(self, index, label, parent=None):
        super().__init__(parent)
        self.POS_OFFSET = QPointF( *([self.POINT_WIDTH/2]*2) )

        ## Model and index

        self._model = index.model()
        self._indexInfo = ( index.row(), index.column(), index.parent() )

        ## Attributes

        self.setPos(self.posAt(0))
        self.setFlags(
            QGraphicsItem.ItemHasNoContents
        )

        ## Child items

        self._createHandleItem(label)

    ## We do not want to draw this item, but paint() and boundingRect() still needs to be implemented.
    ## Give null definitions for both.

    def paint(self, painter, option, widget):
        return None

    def boundingRect(self):
        return QRectF()

    def setPos(self, pos):
        super().setPos(pos)
        self.positionChanged.emit(self, pos)

    def _createHandleItem(self, label):
        t = QTransform()
        t.translate(-self.POS_OFFSET.x(), -self.POS_OFFSET.y())

        handle = Grabber(0, 0, self.POINT_WIDTH, self.POINT_WIDTH, self)
        handle.setPos(QPointF())  
        handle.setTransform(t)
        handle.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        handle.setFlags(QGraphicsItem.ItemIgnoresTransformations)

        label = QGraphicsSimpleTextItem(label, handle)
        label.setPos(self.LABEL_OFFSET)
        label.setFont(QFont())
        label.setBrush(QBrush(Qt.green, Qt.SolidPattern))

        self._labelItem = label

    def _index(self):
        """Returns the QModelIndex of this item."""
        return self._model.index(*self._indexInfo)

    def posAt(self, frame):
        pos = self.loadPos(frame)
        if pos is None:
            prevPos = self.loadPos(self._model.previousValidFrame(frame))
            nextPos = self.loadPos(self._model.nextValidFrame(frame))

            if prevPos is None:
                return nextPos
            if nextPos is None:
                return prevPos
        return pos

    def submitPos(self, pos, frame) -> bool:
        """Changes the position of the joint at frame and update model
        as needed"""
        frameIndex = self._model.frame(frame, self._index())
        return self._model.setData(frameIndex, pos, 'position')

    def loadPos(self, frame):
        """Return the position of this joint at frame. If there is no
        annotation for this frame, returns None"""
        frameIndex = self._model.frame(frame, self._index())
        framePos = self._model.data(frameIndex, 'position')
        return framePos

    def index(self) -> int:
        """The index of this joint"""
        return self._model.jointName(self._index())

    @pyqtSlot()
    def toggleLabel(self):
        if self._labelItem.isVisible():
            self._labelItem.setVisible(False)
        else:
            self._labelItem.setVisible(True)

    @pyqtSlot(int)
    def setFrame(self, frame):
        """Update this point"""
        newPos = self.loadPos(frame)
        if newPos is not None:
            self.setPos(newPos)