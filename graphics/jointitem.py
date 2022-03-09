from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from typing import Dict, List
from . import (
    Controller,
    ControlledItem
)

class JointItem(QGraphicsEllipseItem, ControlledItem):
    LABEL_OFFSET = QPointF(12, -3)
    ready = pyqtSlot()

    @staticmethod
    def getRect(x, y, width, height):
        topLeft = QPointF(x-width/2, y-height/2)
        bottomRight = QPointF(x+width/2, y-height/2)
        return QRectF(topLeft, bottomRight)

    def __init__(self, index, label):
        QGraphicsEllipseItem.__init__(self)

        self._createLabelItem(label)

        ## Attributes

        self._model = index.model()
        self._indexInfo = ( index.row(), index.column(), index.parent() )

        ## Appearance

        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))

        ## Flags

        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setRect(self.getRect(*self.posAt(0), 10, 10))

        self.addListener('setLabelsVisible', self.setLabelVisible)
        
    def _createLabelItem(self, text):
        label = QGraphicsSimpleTextItem(text, self)
        label.setFont(QFont())
        label.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        label.setPos(self.pos() + self.LABEL_OFFSET)

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

    @pyqtSlot(bool)
    def setLabelVisible(self, visible):
        self._labelItem.setVisible(visible)

    @pyqtSlot(int)
    def setFrame(self, frame):
        """Update this joint"""
        newPos = self.loadPos(frame)
        if newPos is not None:
            self.setPos(newPos)