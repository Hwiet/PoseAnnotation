from mediaplayer import MediaPlayer
from joint_item import JointGraphicsItem


from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QOpenGLWidget, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem 
from PyQt5.QtCore import *

from math import pi


class GraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()


    def mouseMoveEvent(self, event):
        QGraphicsScene.mouseMoveEvent(self, event)
        try:
            grabber = self.mouseGrabberItem()

            if grabber is None:
                return

            grabberIndex = self.view.model.index(grabber.index, 1, self.view.currentModelIndex())
            self.view.model.setData(grabberIndex, QVariant(grabber.scenePos()))
        except AttributeError:
            self.view = self.views()[0]


class GraphicsView(QGraphicsView):
    _joint_delegate = JointGraphicsItem

    toPrevFrame = pyqtSignal()
    toNextFrame = pyqtSignal()
    ready = pyqtSignal(QRect)

    def __init__(self, video_file):
        super().__init__()

        ##
        ## private fields
        ##
        self._video = QGraphicsVideoItem()
        self._player = MediaPlayer()


        self._player.setMedia(video_file)
        self._player.setVideoOutput(self._video)
        self._player.setPosition(0)
        self._player.pause()
        

        scene = GraphicsScene()
        scene.addItem(self._video)
        self.setScene(scene)

        self.setAlignment(Qt.AlignCenter) 
        self.fitInView(self._video, Qt.KeepAspectRatioByExpanding)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)


        self._video.nativeSizeChanged.connect(self.changeSize)
        self.toPrevFrame.connect(lambda: self._player.setFrame(self._player.frame() - 1))
        self.toNextFrame.connect(lambda: self._player.setFrame(self._player.frame() + 1))

        self.spaceDown = False
        self.prevMousePos = QPointF()
        self.leftMouseDown = False


    @property
    def model(self):
        return self._model


    def setModel(self, model):
        """Fetches the first set of joints from the model"""

        self._model = model
        poseIndex = None

        for i in range(self.model.rowCount()):
            poseIndex = self.model.index(i, 0)

            if poseIndex.isValid() and self.model.rowCount(poseIndex) > 0:
                break

        for j in range(self.model.rowCount(poseIndex)):
            jointIndex = self.model.index(j, 1, poseIndex)

            position = self.model.data(jointIndex).value()
            jd = self._joint_delegate(j, position)

            jd.setParentItem(self._video)

        # print(len(self.scene().items()))

   
    @pyqtSlot()
    def showPreviousFrame(self):
        self._player.setFrame(self._player.frame() - 1)


    @pyqtSlot()
    def showNextFrame(self):
        self._player.setFrame(self._player.frame() + 1)


    @pyqtSlot()
    def jumpToFrame(self, n):
         self._player.setFrame(n)


    def currentFrame(self):
        return self._player.frame()


    def currentModelIndex(self):
        if not (hasattr(self, '_currentModelIndex') and self._currentModelIndex.isValid()):
            self._currentModelIndex = self.model.index(self.currentFrame(), 0)

        return self._currentModelIndex


    @pyqtSlot()
    def changeSize(self):
        self._video.setSize(self._video.nativeSize())
        self.fitInView(self._video, Qt.KeepAspectRatioByExpanding)
        self.ready.emit(QRect(QPoint(), self._video.nativeSize().toSize()))


    def keyPressEvent(self, event):
        key = event.key()
        dz = 1.1


        if key == Qt.Key_Space:
            self.spaceDown = True


        if key == Qt.Key_Left:
            self.toPrevFrame.emit()


        elif key == Qt.Key_Right:
            self.toNextFrame.emit()


        elif key == Qt.Key_0:
            # return to normal zoom level
            self.resetTransform()


        elif key == Qt.Key_Minus:
            # zoom out
            self.scale(1/dz, 1/dz)


        elif key == Qt.Key_Equal:
            # zoom in
            self.scale(dz, dz)


    def keyReleaseEvent(self, event):
        key = event.key()

        if key == Qt.Key_Space:
            self.spaceDown = False


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