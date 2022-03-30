from typing import List

from PyQt5.QtGui import (
    QPainterPath
)

from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsScene,
    QGraphicsView
)

from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    Qt,
    QObject,
    QVariant,
    QPoint,
    QPointF,
    QSizeF,
    QRect,
    QRectF
)

from PyQt5.QtMultimediaWidgets import (
    QGraphicsVideoItem
)

from math import pi
from models import PoseModel
from . import (
    JointItem,
    EdgeItem
)


class VideoItem(QGraphicsVideoItem):
    def __init__(self):
        super().__init__()


class ItemGroup(QGraphicsItemGroup):
    pass


class PoseView(QGraphicsView):
    viewReady = pyqtSignal(QRect)

    def __init__(self, model, keypoints, chain):
        """_summary_

        Args:
            model (PoseModel): _description_
            keypoints (List[str]): List of keypoint names
            chain (List[List]): List of two-ples defining between which
        keypoints that edges should be drawn 
        """
        super().__init__()

        videoItem = VideoItem()
        scene = QGraphicsScene()
        self._parentItem = videoItem

        scene.addItem(videoItem)
        self.setScene(scene)
        self.setModel(model, keypoints, chain)

        ## Set up signals

        self._parentItem.nativeSizeChanged.connect(self.setSize)

    def setModel(self, model, keypoints, chain, frame=0):
        point = {}
        pointGroup = self.scene().createItemGroup([])
        pointGroup.setParentItem(self._parentItem)
        for i in range(model.poseCount()):
            for j in range(model.jointCount()):
                jointIndex = model.joint(j, i)
                item = JointItem(jointIndex, keypoints[j])
                pointGroup.addToGroup(item)
                point[keypoints[j]] = item

        for c in chain:
            item = EdgeItem(point[c[0]], point[c[1]], self._parentItem)
            item.setZValue(pointGroup.zValue())
            item.stackBefore(pointGroup)
        self._points = pointGroup.childItems()
        self.scene().destroyItemGroup(pointGroup)

    def items(self) -> List[QGraphicsItem]:
        return self._points

    def setScene(self, scene):
        super().setScene(scene)

    def fitInView(self):
        super().fitInView(self._parentItem, Qt.KeepAspectRatio)

    def videoItem(self):
        return self._parentItem

    def setLabelsVisible(self, visible):
        self.emit('setLabelsVisible', visible)

    def wheelEvent(self, event):
        dz = 0.2
        degrees = event.angleDelta().y() / 8
        rad = degrees * pi / 180
        x = rad * dz + 1

        self.scale(x, x)
        self.centerOn(event.pos())

    @pyqtSlot(QSizeF)
    def setSize(self, size):
        self._parentItem.setSize(size)
        self.scene().setSceneRect(QRectF(self._center(size, size*10), size*10))
        self.fitInView()
        self.viewReady.emit(QRect(QPoint(), self._parentItem.nativeSize().toSize()))

    def zoomOut(self):
        dz = 1.1
        self.scale(1/dz, 1/dz)

    def zoomIn(self):
        dz = 1.1
        self.scale(dz, dz)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
    
    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space and not event.isAutoRepeat():
            self.setDragMode(QGraphicsView.NoDrag)

    def _center(self, size1, size2):
        xOffset = (size1.width() - size2.width()) / 2
        yOffset = (size1.height() - size2.height()) / 2
        return QPointF(xOffset, yOffset)