from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from typing import Dict, List

from PyQt5.QtCore import (
    QPointF,
    QRectF
)

from . import ControlledItem

class JointGraphicsItem(QGraphicsEllipseItem, ControlledItem):
    LABEL_OFFSET = QPointF(12, -3)

    @staticmethod
    def getRect(x, y, width, height):
        topLeft = QPointF(x-width/2, y-height/2)
        bottomRight = QPointF(x+width/2, y-height/2)
        return QRectF(topLeft, bottomRight)

    def __init__(self, index):
        QGraphicsEllipseItem.__init__(self)
        ## Attributes

        self._model = index.model()
        self._indexInfo = ( index.row(), index.column(), index.parent() )

        ## Appearance

        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))

        ## Flags

        self.setFlags(QGraphicsItem.ItemIsMovable)

        ## Set up

        self.createLabelItem()

    def _index(self):
        """Returns the QModelIndex of this item."""
        return self._model.index(*self._indexInfo)

    def setPos(self, pos, frame) -> bool:
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

    def linear(self):
        pass

    def index(self) -> int:
        """The index of this joint"""
        return self._model.jointName(self._index())

    def label(self) -> str:
        """The label of this joint corresponding to its name"""
        return self._model.jointLabel(self._index())

    def createLabelItem(self):
        label = QGraphicsSimpleTextItem(self.label(), self)
        label.setFont(QFont())
        label.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        label.setPos(self.pos() + self.LABEL_OFFSET)
        return label