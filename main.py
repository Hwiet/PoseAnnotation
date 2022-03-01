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

from models.pose_model import PoseModel
from mediaplayer import MediaPlayer

import pandas as pd
import cv2
from collections import namedtuple

from PyQt5.QtCore import QObject, QRect

from views.graphicsview import GraphicsView
from widgets.frame_status import FrameStatus



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
    Action = namedtuple('Action', ['name', 'keySequence', 'slot'], defaults=(None, None))


    def __init__(self, parent: QWidget=None):
        super().__init__(parent)

        self.addMenu(
            self.newMenu(
                'File',
                (
                    Action(
                        'Save', QKeySequence.Save
                    ),
                    Action(
                        'Revert'
                    ),
                    Action(
                        'Quit', QKeySequence(Qt.CTRL + Qt.Key_Q),
                        lambda: QApplication.quit()
                    )
                )
            )
        )

        self.addMenu(
            self.newMenu(
                'Edit',
                (
                    Action(
                        'Undo', QKeySequence.Undo
                    ),
                    Action(
                        'Redo', QKeySequence.Redo
                    )
                )
            )
        )

        self.addMenu(
            self.newMenu(
                'View',
                (
                    Action(
                        'Zoom In', QKeySequence.ZoomIn,
                        graphics.zoomIn
                    ),
                    Action(
                        'Zoom Out', QKeySequence.ZoomOut,
                        graphics.zoomOut
                    ),
                    Action(
                        'Fit on Screen', QKeySequence(Qt.CTRL + Qt.Key_0),
                        graphics.fitInView
                    )
                )
            )
        )

        self.prevFrameAct  =  Action(
                        'Previous Frame', QKeySequence(Qt.Key_Left),
                        graphics.showPreviousFrame
                    )

        self.addMenu(
            self.newMenu(
                'Navigate',
                (
                   ,
                    Action(
                        'Next Frame', QKeySequence(Qt.Key_Right),
                        graphics.showNextFrame
                    ),
                    Action(
                        'Jump to Frame', slot=jumpToFrame
                    )
                )
            )
        )

        # self.addMenu(
        #     self.newMenu(
        #         'Playback',
        #         (
        #             Action(
        #                 'Play'
        #             )
        #         )
        #     )
        # )

    def newMenu(self, menuName, actions):
        menu = QMenu(menuName)

        for action in actions:
            x = menu.addAction(action.name)

            if action.keySequence is not None:
                x.setShortcut(action.keySequence)
            if action.slot is not None:
                x.triggered.connect(action.slot)

            menu.addAction(x)

        return menu


    def newAction(self, text, keySequence=None, slot=None):
        action = QAction(text)
        if keySequence is not None:
            action.setShortcut(keySequnce)
        if slot is not None:
            action.triggered.connect(slot)

        return action


    def onPositionChange(self):
        # can go to previous frame after position change?
        if player.frame() - 1 >= 0:
            self.prevFrameAct.setEnabled(True)

            if player.frame() + 1 < player.frameCount():
                self.nextFrameAct.setEnabled(True)
            else:
                self.nextFrameAct.setEnabled(False)
        else:
            self.prevFrameAct.setEnabled(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        graphics.setJointModels(jointModels)
        self.setCentralWidget(graphics)

        frameCount = player.frameCount()
        frameStat = FrameStatus(player)
        self.statusBar().addWidget(frameStat)

        self.player = MediaPlayer()
        self.graphics = GraphicsView('data/media/Golf Swing 0.mp4', self.player)

        self.graphics.setModel(PoseModel(media.poses))
        self.setCentralWidget(self.graphics)

        fileMenu = self.menuBar().addMenu('File')
        editMenu = self.menuBar().addMenu('Edit')
        viewMenu = self.menuBar().addMenu('View')

        frameCount = self.graphics.frameCount()
        frameStat = FrameStatus(self.player)
        self.statusBar().addWidget(frameStat)

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