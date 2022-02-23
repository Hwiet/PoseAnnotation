import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


from annotated_media import AnnotatedVideo
from custom_annotation import CustomFormat

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem 
from PyQt5.QtWidgets import *

from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex, QVariant, QMetaType, QPointF, QSizeF, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItemModel


from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir, QUrl

from pose_model import PoseModel
from mediaplayer import MediaPlayer

import pandas as pd
import cv2

from PyQt5.QtCore import QObject, QRect

from graphicsview import GraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        keyframes = pd.read_pickle('data/golfDB.pkl').loc[0]['events']
        keyframes = [frame - keyframes[0] for frame in keyframes]
        keyframes.pop(0)
        keyframes.pop(len(keyframes) - 1)

        media = AnnotatedVideo('data/media/Golf Swing 0.mp4', CustomFormat('data/annotation/Golf Swing 0.txt'), keyframes)

        self.graphics = GraphicsView('data/media/Golf Swing 0.mp4')
        self.setCentralWidget(self.graphics)

        fileMenu = self.menuBar().addMenu('File')
        editMenu = self.menuBar().addMenu('Edit')
        viewMenu = self.menuBar().addMenu('View')

        sjafsdl = self.statusBar().showMessage('Golf Swing 0')

        navigateMenu = self.menuBar().addMenu('Navigate')
        navigateMenu.addAction('Jump to frame', self.jumpToFrame)


    def jumpToFrame(self):
        frame, ok = QInputDialog.getInt(self, 'Jump to frame', 'Frame', self.graphics.currentFrame(), 0, 1000)
        if ok:
            self.graphics.jumpToFrame(frame)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())