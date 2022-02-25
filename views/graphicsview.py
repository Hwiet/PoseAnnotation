from mediaplayer import MediaPlayer
from views.joint_item import JointGraphicsItem


from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem 
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence, QBitmap, QPainter, QPen

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


        # fitOnScreenShortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_0), self)
        # fitOnScreenShortcut.activated.connect(lambda: self.fitInView(self._video, Qt.KeepAspectRatio))


        # fitOnScreenAct = QAction('Fit on Screen')
        # fitOnScreenAct.setShortcuts()
        # fitOnScreenAct.acti

    def fitInView(self):
        super().fitInView(self._video, Qt.KeepAspectRatio)


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
            jd = self._joint_delegate(j, position, QPersistentModelIndex(jointIndex))

            jd.setParentItem(self._video)

        # print(len(self.scene().items()))

    def paintEvent(self, event):
        super().paintEvent(event)

        if hasattr(self, 'paintSurface'):
            painter = QPainter(self.paintSurface)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(0, 0, 585, 685)


    def _updateJoints(self, n):
        for joint in self._video.childItems():
            joint.show()
            modelIndex = joint.modelIndex
            row = modelIndex.row()
            column = modelIndex.column()

            try:
                from_ = self._model.index(row, column, modelIndex.parent())
                to = self._model.index(row, column, modelIndex.parent().siblingAtRow(n))
                self._model.changePersistentIndex(from_, to)
                joint.setPos(self.model.data(modelIndex).value())
            except:
                joint.hide()

   
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


    @pyqtSlot()
    def jumpToFrame(self, n):
         self._player.setFrame(n)


    def currentFrame(self):
        return self._player.frame()


    def frameCount(self):
        return self._player.frameCount()


    def currentModelIndex(self):
        if not (hasattr(self, '_currentModelIndex') and self._currentModelIndex.isValid()):
            self._currentModelIndex = self.model.index(self.currentFrame(), 0)

        return self._currentModelIndex


    def zoomOut(self):
        dz = 1.1
        self.scale(1/dz, 1/dz)


    def zoomIn(self):
        dz = 1.1
        self.scale(dz, dz)


    @pyqtSlot()
    def changeSize(self):
        self._video.setSize(self._video.nativeSize())
        bitmap = QBitmap(self._video.nativeSize().toSize())
        bitmap.clear()
        self.paintDevice = QWidget()
        self.paintDevice.setAttribute(Qt.WA_TranslucentBackground, True)
        self.paintDevice.setMinimumSize(self._video.nativeSize().toSize())
        widgetItem = self.scene().addWidget(self.paintDevice)
        widgetItem.setParentItem(self._video)
        self.fitInView()
        self.ready.emit(QRect(QPoint(), self._video.nativeSize().toSize()))


    def keyPressEvent(self, event):
        key = event.key()
        dz = 1.1

        if key == Qt.Key_Space:
            self.spaceDown = True
            if self._player.state() == MediaPlayer.StoppedState \
                or self._player.state() == MediaPlayer.PausedState:
                self._player.play()
            else:
                self._player.pause()


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