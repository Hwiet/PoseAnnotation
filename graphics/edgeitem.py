from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import QLineF
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush
from graphics.controller import ControlledItem


class EdgeItem(QGraphicsLineItem, ControlledItem):
    def __init__(self, from_, to_):
        """QGraphicsLineItem that attaches each of its endpoints to another item.

        Arguments:
        from_: Item to attach to endpoint 1
        to_: Item to attach to endpoint 2
        """
        super(EdgeItem, self).__init__()

        self._from = from_
        self._to = to_
        
        self._p1 = QPointF()
        self._p2 = QPointF()
        
        self.setPen(QPen(QBrush(Qt.red), 2))
        self.setLine(QLineF(from_.scenePos(), to_.scenePos()))

        from_.addListener('positionChanged', self._update)
        to_.addListener('positionChanged', self._update)

    def _update(self, item, newPosition):
        """Event handler to reposition one of this line's endpoints if needed.

        Args:
            item (ControlledItem): Item that fired the 'positionChanged' event.
            newPosition (QPointF): The new position of the item.
        """
        if item is self._from:
            self._p1 = newPosition
            if not self._p2.isNull():
                self.setLine(QLineF(self._p1, self._p2))
        elif item is self._to:
            self._p2 = newPosition
            if not self._p1.isNull():
                self.setLine(QLineF(self._p1, self._p2))