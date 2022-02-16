import sys

from joint_item import JointGraphicsItem
from mediaplayer import MediaPlayer
from graphicsview import GraphicsView


from PyQt5.QtWidgets import QAbstractItemView, QGraphicsView, QGraphicsScene, QGraphicsItemGroup, QGraphicsItem
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem 
from PyQt5.QtCore import QPersistentModelIndex, Qt, pyqtSignal, pyqtSlot, QVariant


class PoseView(QAbstractItemView):
    sceneItemsReady = pyqtSignal()


    def __init__(self, video_file):
        super().__init__()

        self._joint_delegate = JointGraphicsItem
        self._items = list()

        self.setViewport(GraphicsView(QGraphicsScene()))

        self._video_output = QGraphicsVideoItem()
        self._media_player = self.initializeMediaPlayer(
                self._video_output,
                video_file
            )

        self._media_player.setPosition(0)
        self._media_player.pause()


        self.viewport().show()


        # signals
        self.viewport().toPrevFrame.connect(self.showPreviousFrame)
        self.viewport().toNextFrame.connect(self.showNextFrame)
        self.sceneItemsReady.connect(self.setUpScene)


    def initializeMediaPlayer(self, output, media):
        media_player = MediaPlayer()
        media_player.setVideoOutput(output)
        media_player.setMedia(media)

        return media_player


    @property
    def model(self):
        try:
            return self._model
        except NameError:
            print("attribute _model is not defined.", file=sys.stderr)


    def setModel(self, model):
        self._model = model

        for i in range(self.model.rowCount()):
            poseIndex = self.model.index(i, 0)

            for j in range(self.model.rowCount(poseIndex)):
                jointIndex = self.model.index(j, 0, poseIndex)
                position = self.model.data(jointIndex)
                
                jd = self._joint_delegate(j, *position)
                self._item.append(jd)


    @property 
    def items(self):
        return self._items

    
    def frame(self):
        self._media_player.frame()


    @pyqtSlot()
    def showPreviousFrame(self):
        self._media_player.setFrame(self._media_player.frame() - 1)


    @pyqtSlot()
    def showNextFrame(self):
        self._media_player.setFrame(self._media_player.frame() + 1)


    @pyqtSlot(QGraphicsItem, int, int)
    def updateJointPosition(self, item, x, y):
        poseIndex = self.model.index(frame, 0)
        if not self.model.setData(jointIndex, [x, y]):
            print("Cannot update joint position", file=sys.stderr)

    
    @pyqtSlot()
    def setUpScene(self):
        self.viewport().scene().addItem(self._video_output)

        for item in self._items:
            self.viewport().scene().addItem(item)
            item.posChanged.connect(self.updateJointPosition)