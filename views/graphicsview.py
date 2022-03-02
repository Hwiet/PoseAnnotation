from mediaplayer import MediaPlayer
from views.joint_item import *


from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem 
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence, QBitmap, QPainter, QPen

from math import pi


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()


    def mouseMoveEvent(self, event):
        # keep behavior of mouseMoveEvent from super class
        QGraphicsScene.mouseMoveEvent(self, event)
        
        grabber = self.mouseGrabberItem()

        if isinstance(grabber, JointGraphicsItem):
            grabber.setData(QVariant(event.scenePos()))


class GraphicsView(QGraphicsView):
    _joint_delegate = JointGraphicsItem

    ready = pyqtSignal(QRect)

    def __init__(self, video_file, mediaplayer):
        super().__init__()

        ##
        ## private fields
        ##
        self._video = QGraphicsVideoItem()
        self._player = mediaplayer


        self._player.setMedia(video_file)
        self._player.setVideoOutput(self._video)
        self._player.setPosition(0)
        self._player.pause()
        

        scene = GraphicsScene()
        scene.addItem(self._video)
        self.setScene(scene)

        self.setAlignment(Qt.AlignCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)


        self._video.nativeSizeChanged.connect(self.changeSize)

        self.spaceDown = False
        self.prevMousePos = QPointF()
        self.leftMouseDown = False
            

    def registerSS(self, ss):
        ss.signal.connect(ss.slot)

    def fitInView(self):
        super().fitInView(self._video, Qt.KeepAspectRatio)


    def setPoseModel(self, model):
        self._poseModel = model


    def setJointModels(self, models):
        jointItems = list()

        for i in range(len(models)):
            jointItem = self._joint_delegate(i, models[i])
            jointItem.setParentItem(self._video)
            jointItems.append(jointItem)
        self._jointItems = jointItems

        x = (
            (0, 1),
            (1, 3),
            (0, 2),
            (2, 4),
            (0, 5),
            (5, 7),
            (7, 9),
            (5, 11),
            (11, 13),
            (13, 15),
            (0, 6),
            (6, 8),
            (8, 10),
            (6, 12),
            (12, 14),
            (14, 16)
        )

        for y in x:
            edge = EdgeItem(jointItems[y[0]], jointItems[y[1]])
            edge.setParentItem(self._video)

            jointItems[y[0]].emit('positionChanged', jointItems[y[0]], jointItems[y[0]].scenePos())
            jointItems[y[1]].emit('positionChanged', jointItems[y[1]], jointItems[y[1]].scenePos())

    @pyqtSlot(bool)
    def showLabels(self, doShow):
        print('caled')
        if doShow:
            for joint in self._jointItems:
                joint.showLabel()
        else:
            for joint in self._jointItems:
                joint.hideLabel()

    @pyqtSlot()
    def showPreviousFrame(self):
        prevFrame = self._player.frame() - 1
        self._player.setFrame(prevFrame)
        self._updateJoints(prevFrame)


    @pyqtSlot()
    def showNextFrame(self):
        nextFrame = self._player.frame() + 1
        self._player.setFrame(nextFrame)
        self._updateJoints(nextFrame)


    @pyqtSlot(int)
    def showFrame(self, n):
        self._player.setFrame(n)
        self._updateJoints(n)


    def _updateJoints(self, frame):
        for joint in self._jointItems:
            joint.setPosAt(frame)


    def zoomOut(self):
        dz = 1.1
        self.scale(1/dz, 1/dz)


    def zoomIn(self):
        dz = 1.1
        self.scale(dz, dz)


    @pyqtSlot()
    def changeSize(self):
        self._video.setSize(self._video.nativeSize())
        self.fitInView()
        self.ready.emit(QRect(QPoint(), self._video.nativeSize().toSize()))


    def mouseDownEvent(self, event):
        QGraphicsView.mouseDownEvent(self, event)
        if event.button() is Qt.LeftButton:
            self.prevMousePos = event.globalPos()
            self.leftMouseDown = True


    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() is Qt.LeftButton:
            self.prevMousePos = QPointF()
            self.leftMouseDown = False


    def mouseMoveEvent(self, event):
        QGraphicsView.mouseMoveEvent(self, event)
        super().mouseMoveEvent(event)
        if (event.buttons() & Qt.LeftButton) and self.spaceDown:
            delta = event.globalPos() - self.prevMousePos
            print(f"{delta.x()}, {delta.y()}")
            self.prevMousePos = event.globalPos()

            self.translate(delta.x(), delta.y())


    def wheelEvent(self, event):
        dz = 0.2
        degrees = event.angleDelta().y() / 8
        rad = degrees * pi / 180
        x = rad * dz + 1

        self.scale(x, x)
        self.centerOn(event.pos())