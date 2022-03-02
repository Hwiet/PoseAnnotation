from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial
from typing import Dict, List


POSITION = Qt.UserRole+1


class Controller(QObject):
    __instance = None
    __signal: Dict[str, List[partial]] = None

    positionChanged = pyqtSignal(QGraphicsItem, QPointF)

    @staticmethod
    def getInstance():
        if Controller.__instance is None:
            Controller()
        return Controller.__instance

    def __init__(self):
        if Controller.__instance is None:
            Controller.__instance = self
            Controller.__signal = dict()
        else:
            raise Exception(f'Cannot create another instance of a singleton class {self.__name__}')

    def registerListener(self, name, functor):
        if not Controller.__signal.__contains__(name):
            Controller.__signal[name] = list()
        Controller.__signal[name].append(functor)

    def removeListener(self, name, functor):
        Controller.__signal[name].remove(functor)

    def fire(self, name, *args):
        for p in Controller.__signal[name]:
            p = partial(p, *args)
            p()


class __ControlledItem(QGraphicsItem):
    def addListener(self, name: str, functor):
        Controller.getInstance().registerListener(name, functor)

    def removeListener(self, name: str, functor):
        Controller.getInstance().removeListener(name, functor)

    def emit(self, name, *args):
        Controller.getInstance().fire(name, *args)


class EdgeItem(QGraphicsLineItem, __ControlledItem):
    def __init__(self, from_, to_):
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
        if item is self._from:
            self._p1 = newPosition
            if not self._p2.isNull():
                self.setLine(QLineF(self._p1, self._p2))
        elif item is self._to:
            self._p2 = newPosition
            if not self._p1.isNull():
                self.setLine(QLineF(self._p1, self._p2))


class JointGraphicsItem(QGraphicsEllipseItem, __ControlledItem):
    def __init__(
            self,
            jointIndex: int,
            model: QAbstractItemModel,
            currentFrame: int=0):
        point = model.data(model.index(0, 1), POSITION)
        super(JointGraphicsItem, self).__init__(QRectF(point, point + QPointF(10, 10)))


        self._jointIndex = jointIndex
        self._model = model
        self._modelIndex = self.model.index(0, 1)
        self.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        self.setFlags(QGraphicsItem.ItemIsMovable)

        self._label = QGraphicsSimpleTextItem('asdfasdf', self)
        self._label.setPos(self.pos() + QPointF(12, -3))
        self._label.setFont(QFont())
        self._label.setBrush(QBrush(Qt.green, Qt.SolidPattern))

    @property
    def model(self):
        return self._model

    @property
    def jointIndex(self):
        return self._jointIndex

    @property
    def modelIndex(self) -> QModelIndex:
        """
        Returns model index located at row=frameNum and column=1
        Convert private field `_modelIndex` from QPersistentModelIndex to
        QModelIndex
        """
        return self._modelIndex.model().index(
            self._modelIndex.row(),
            self._modelIndex.column()
        )

    @modelIndex.setter
    def modelIndex(self, index: QModelIndex):
        self._modelIndex = QPersistentModelIndex(index)

    @property
    def currentFrame(self) -> int:
        # row number = frame number
        return self._modelIndex.row()

    @currentFrame.setter
    def currentFrame(self, frame: int):
        """Update values of this item to correspond to frame"""
        self.modelIndex = self.modelIndex.siblingAtRow(frame)
        self.setPosAt(frame)

    def pos(self):
        super_ = super().pos()
        if super_.isNull():
            return self.mapToParent(self._modelIndex.data(POSITION))
        return super_

    def scenePos(self):
        super_ = super().scenePos()
        if super_.isNull():
            return self.modelIndex.data(POSITION)
        return super_

    def showLabel(self):
        self._label.show()

    def hideLabel(self):
        self._label.hide()
            
    def _linear(
            self,
            t: int,
            tMin: int,
            tMax: int,
            value1, value2):
        """Interpolate linearly over time"""
        progress = (t - tMin) / (tMax - tMin)
        if isinstance(value1, QPointF) and isinstance(value2, QPointF):
            if t == tMin:
                return value1
            elif t == tMax:
                return value2

            dx = ( value2.x() - value1.x() ) * progress
            dy = ( value2.y() - value1.y() ) * progress

            return QPointF(
                value1.x() + dx,
                value1.y() + dy
            )
        else:
            raise ValueError(f'Cannot interpolate values of {value1.type()}')

    def _previousValidIndex(self, frame):
        if self.modelIndex.row() <= 0:
            return QModelIndex()

        previousModelIndex = self._model.index(
            self.modelIndex.row()-1,
            self.modelIndex.column()
        )

        for i in range(previousModelIndex.row(), -1, -1):
            if previousModelIndex.row() != QModelIndex():
                # found a valid index, break out of search loop
                break

            # decrement
            previousModelIndex = previousModelIndex.siblingAtRow(
                previousModelIndex.row()-1,
            )

        if previousModelIndex.row() == QModelIndex():
            # could not find valid index, return invalid index
            return QModelIndex()
        else:
            return previousModelIndex

    def _nextValidIndex(self, frame) -> QModelIndex:
        nextModelIndex = self._model.index(
            self.modelIndex.row()+1,
            self.modelIndex.column()
        )

        for i in range(nextModelIndex.row(), self._model.rowCount()):
            print(nextModelIndex.data(POSITION))
            if nextModelIndex.data(POSITION) != QVariant():
                # found a valid index, break out of search loop
                break

            # increment
            nextModelIndex = nextModelIndex.siblingAtRow(
                nextModelIndex.row()+1,
            )

        if nextModelIndex.row() == QModelIndex():
            # could not find valid index, return invalid index
            return QModelIndex()
        else:
            return nextModelIndex

    def frame(self, index: QModelIndex):
        """return frame that corresponds to this index"""
        return index.row()

    def setPosAt(self, frame: int) -> QPointF:
        """
        Updates the position of the joint in the scene according to the given
        frame. This method _does not_ update data in memory.
        """
        matches = self._model.match(
            self.modelIndex.siblingAtRow(frame),
            Qt.UserRole+1,
            QVariant(frame))
        
        newPos = None
        if matches != []:
            # found a match, return position
            newPos = matches[0].data(Qt.UserRole+1)
            self.setPos(newPos)
        else:
            # try to find values before and after this frame
            prev_ = self._previousValidIndex(frame)
            next_ = self._nextValidIndex(frame)
            # print(f'{prev_.row()}, {next_.row()}')

            if not prev_.isValid():
                newPos = next_.data(Qt.UserRole+1)
            elif not next_.isValid():
                newPos = prev_.data(Qt.UserRole+1)
            else:
                newPos = self._linear(
                    t=frame,
                    tMin=prev_.row(),
                    tMax=next_.row(),
                    value1=prev_.data(Qt.UserRole+1),
                    value2=next_.data(Qt.UserRole+1)
                )

        self.modelIndex = self.modelIndex.siblingAtRow(frame)
        self.setPos(newPos)
        self.emit('positionChanged', self, newPos)
        return newPos

    def setData(
            self,
            value: QVariant) -> None:
        """
        Updates the joint position in the current frame in memory
        """
        self._model.setData(self._modelIndex, value)
        self.emit('positionChanged', self, value.value().toPoint())

    @pyqtSlot(int)
    def onFrameChange(self, frame):
        self.currentFrame = frame