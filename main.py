import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


from annotated_media import AnnotatedVideo
from custom_annotation import CustomFormat

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem 
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QAbstractScrollArea, QGraphicsWidget, QGraphicsProxyWidget

from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex, QVariant, QMetaType, QPointF, QSizeF
from PyQt5.QtGui import QStandardItemModel


from PyQt5.QtCore import Qt
from PyQt5.QtCore import QDir, QUrl

from pose_model import PoseModel
from pose_view import PoseView

import pandas as pd
import cv2

from PyQt5.QtCore import QObject


if __name__ == '__main__':
    app = QApplication(sys.argv)


    keyframes = pd.read_pickle('data/golfDB.pkl').loc[0]['events']
    keyframes = [frame - keyframes[0] for frame in keyframes]
    keyframes.pop(0)
    keyframes.pop(len(keyframes) - 1)

    media = AnnotatedVideo('data/media/Golf Swing 0.mp4', CustomFormat('data/annotation/Golf Swing 0.txt'), keyframes)

    pose_model = PoseModel(media.poses[0])

    scene = QGraphicsScene()

    display = QGraphicsVideoItem()

    display.nativeSizeChanged.connect(lambda: display.setSize(display.nativeSize()))

    player = QMediaPlayer()
    player.setVideoOutput(display)
    player.setMedia(QMediaContent(QUrl('data/media/Golf Swing 0.mp4')))
    player.setPosition(0)
    player.pause()

    scene.addItem(display)

    pose_view = PoseView()
    pose_view.setModel(pose_model)

    for item in pose_view.items:
        scene.addItem(item)

    view = QGraphicsView(scene)

    view.show()


    sys.exit(app.exec_())