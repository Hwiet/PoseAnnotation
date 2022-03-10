from PyQt5.QtCore import (
    pyqtSlot,
    Qt,
    QPointF,
    QLineF,
    QRectF
)

from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush

from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsLineItem
)

class EdgeItem(QGraphicsObject):
    def __init__(self, from_, to_, parent=None):
        """QGraphicsLineItem that attaches each of its endpoints to another item.

        Arguments:
        from_: Item to attach to endpoint 1
        to_: Item to attach to endpoint 2
        """
        super().__init__(parent)
        self.setFlags(QGraphicsItem.ItemHasNoContents)
        
        self._line = QGraphicsLineItem(parent)

        self._from = from_
        self._to = to_
        
        self._p1 = QPointF()
        self._p2 = QPointF()
        
        #  Cosmetic pens are used to draw strokes that have a constant
        #  width regardless of any transformations applied to the
        #  QPainter they are used with. Drawing a shape with a cosmetic
        #  pen ensures that its outline will have the same thickness at
        #  different scale factors.A zero width pen is cosmetic by
        #  default.
        pen = QPen(Qt.red)
        pen.setWidth(0)

        self._line.setPen(pen)
        self._line.setLine(QLineF(from_.pos(), to_.pos()))

        from_.positionChanged.connect(self._updateLine)
        to_.positionChanged.connect(self._updateLine)

    def paint(self, painter, option, widget):
        return None

    def boundingRect(self):
        return QRectF()

    @pyqtSlot(QGraphicsItem, QPointF)
    def _updateLine(self, item, newPosition):
        """Event handler to reposition one of this line's endpoints if needed.

        Args:
            item (ControlledItem): Item that fired the 'positionChanged' event.
            newPosition (QPointF): The new position of the item.
        """
        if item is self._from:
            self._p1 = newPosition
            if not self._p2.isNull():
                self._line.setLine(QLineF(self._p1, self._p2))
        elif item is self._to:
            self._p2 = newPosition
            if not self._p1.isNull():
                self._line.setLine(QLineF(self._p1, self._p2))