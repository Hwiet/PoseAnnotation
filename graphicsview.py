from mediaplayer import MediaPlayer


from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QOpenGLWidget
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem 
from PyQt5.QtCore import *


class GraphicsView(QGraphicsView):
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
        

        scene = QGraphicsScene()
        scene.addItem(self._video)
        self.setScene(scene)

        self.setAlignment(Qt.AlignCenter) 
        self.fitInView(self._video, Qt.KeepAspectRatioByExpanding)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)


        self._video.nativeSizeChanged.connect(self.changeSize)
        self.toPrevFrame.connect(lambda: self._player.setFrame(self._player.frame() - 1))
        self.toNextFrame.connect(lambda: self._player.setFrame(self._player.frame() + 1))

   
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


    @pyqtSlot()
    def changeSize(self):
        self._video.setSize(self._video.nativeSize())
        self.fitInView(self._video, Qt.KeepAspectRatioByExpanding)
        self.ready.emit(QRect(QPoint(), self._video.nativeSize().toSize()))


    def keyPressEvent(self, event):
        key = event.key()
        dz = 1.1


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