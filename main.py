import sys

from annotated_media import AnnotatedVideo
from custom_annotation import CustomFormat

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from models.pose_model import PoseModel
from mediaplayer import MediaPlayer

import pandas as pd
import cv2


from views.graphicsview import GraphicsView
from widgets.frame_status import FrameStatus
from collections import namedtuple



SlotSignalPair = namedtuple('SlotSignalPair', ['signal', 'slot'])

def jumpToFrame(self):
    frame, ok = QInputDialog.getInt(
        window,
        'Jump to frame',
        'Frame',
        player.frame(),
        0, 1000
    )

    if ok: player.setFrame(frame)



class MenuBar(QMenuBar):
    def __init__(self, parent: QWidget=None):
        super().__init__(parent)


        fileMenu = QMenu('File', self)
        fileMenu.addAction(
            QIcon(),
            'Save',
        )
        fileMenu.addAction(
            QIcon(),
            'Revert'
        )
        fileMenu.addAction(
            QIcon(),
            'Quit',
            lambda: QApplication.quit(),
            QKeySequence(Qt.CTRL + Qt.Key_Q)
        )
        self.addMenu(fileMenu)


        editMenu = QMenu('Edit', self)
        editMenu.addAction(
            QIcon(),
            'Undo',
        )
        editMenu.addAction(
            QIcon(),
            'Redo'
        )
        self.addMenu(editMenu)


        viewMenu = QMenu('View', self)
        viewMenu.addAction(
            QIcon(),
            'Zoom In',
            graphics.zoomIn,
            QKeySequence.ZoomIn
        )
        viewMenu.addAction(
            QIcon(),
            'Zoom Out',
            graphics.zoomOut,
            QKeySequence.ZoomOut
        )
        viewMenu.addAction(
            QIcon(),
            'Fit on Screen',
            graphics.fitInView,
            QKeySequence(Qt.CTRL + Qt.Key_0)
        )
        viewMenu.addSeparator()
        d = viewMenu.addAction(
            QIcon(),
            'Show labels',
        )
        d.setCheckable(True)
        slotSignalPairs.append(SlotSignalPair(signal=d.toggled, slot=graphics.showLabels))
        self.addMenu(viewMenu)


        navMenu = QMenu('Navigate', self)
        self._prevFrameAct = navMenu.addAction(
            QIcon(),
            'Previous Frame',
            graphics.showPreviousFrame,
            QKeySequence(Qt.Key_Left)
        )
        self._nextFrameAct = navMenu.addAction(
            QIcon(),
            'Next Frame',
            graphics.showNextFrame,
            QKeySequence(Qt.Key_Right)
        )
        navMenu.addAction(
            QIcon(),
            'Jump to Frame',
            jumpToFrame
        )
        self.addMenu(navMenu)


    def onPositionChange(self):
        # can go to previous frame after position change?
        if player.frame() - 1 >= 0:
            self._prevFrameAct.setEnabled(True)

            if player.frame() + 1 < player.frameCount():
                self._nextFrameAct.setEnabled(True)
            else:
                self._nextFrameAct.setEnabled(False)
        else:
            self._prevFrameAct.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        graphics.setJointModels(jointModels)
        self.setCentralWidget(graphics)

        frameCount = player.frameCount()
        frameStat = FrameStatus(player)
        self.statusBar().addWidget(frameStat)

        self.setMenuBar(MenuBar())


        player.positionChanged.connect(self.menuBar().onPositionChange)


app = QApplication(sys.argv)

keyframes = pd.read_pickle('data/golfDB.pkl').loc[0]['events']
keyframes = [frame - keyframes[0] for frame in keyframes]
keyframes.pop(0)
keyframes.pop(len(keyframes) - 1)

media = AnnotatedVideo('data/media/Golf Swing 0.mp4', CustomFormat('data/annotation/Golf Swing 0.txt'), keyframes)

poseModel = QStandardItemModel()
jointModels = list([QStandardItemModel() for i in range(17)])

for pose in media.poses:
    poseData = pose.data

    if poseData == list():
        poseModel.appendRow(QStandardItem())

    else:
        row = media.poses.index(pose)

        items = [QStandardItem(), QStandardItem()]
        items[0].setData(QVariant(row), Qt.UserRole+1)
        items[1].setData(QVariant(poseData['confidence']), Qt.UserRole+1)

        poseModel.appendRow(items)

    for joint in pose.joints:
        tableIndex = int(joint.data['name'])
        if poseData == list():
            jointModels[tableIndex].appendRow(QStandardItem())

        items = [QStandardItem(), QStandardItem()]
        items[0].setData(QVariant(row), Qt.UserRole+1)
        items[1].setData(QVariant(QPointF(*joint.position)), Qt.UserRole+1)

        jointModels[tableIndex].appendRow(items)

slotSignalPairs = []


player = MediaPlayer()
graphics = GraphicsView('data/media/Golf Swing 0.mp4', player)

window = MainWindow()
graphics.registerSS(slotSignalPairs[0])
window.showMaximized()

sys.exit(app.exec_())