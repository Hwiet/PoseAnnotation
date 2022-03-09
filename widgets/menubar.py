from PyQt5.QtCore import (
    Qt,
    pyqtSignal
)

from PyQt5.QtWidgets import (
    QMenuBar,
    QMenu
)

from PyQt5.QtGui import (
    QIcon,
    QKeySequence
)


class MenuBar(QMenuBar):

    # File

    quitApplication = pyqtSignal()
    save = pyqtSignal()
    saveAs = pyqtSignal()
    saveAsCopy = pyqtSignal()
    revert = pyqtSignal()
    import_ = pyqtSignal()

    # View

    zoomIn = pyqtSignal()
    zoomOut = pyqtSignal()
    fitOnScreen = pyqtSignal()
    toggleLabels = pyqtSignal()

    # Navigation

    goToPreviousFrame = pyqtSignal()
    goToNextFrame = pyqtSignal()
    goToFrame = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)


        fileMenu = QMenu('File', self)
        fileMenu.addAction(
            QIcon(),
            'Save',
        )
        fileMenu.addAction(
            QIcon(),
            'Open',
            
            # QKeySequence.Open
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
            lambda: self.zoomIn.emit(),
            QKeySequence.ZoomIn
        )
        viewMenu.addAction(
            QIcon(),
            'Zoom Out',
            lambda: self.zoomOut.emit(),
            QKeySequence.ZoomOut
        )
        viewMenu.addAction(
            QIcon(),
            'Fit on Screen',
            lambda: self.fitOnScreen.emit(),
            QKeySequence(Qt.CTRL + Qt.Key_0)
        )
        viewMenu.addSeparator()
        d = viewMenu.addAction(
            QIcon(),
            'Show labels',
            lambda: self.toggleLabels.emit()
        )
        d.setCheckable(True)
        # slotSignalPairs.append(SlotSignalPair(signal=d.toggled, slot=graphics.showLabels))
        self.addMenu(viewMenu)


        navMenu = QMenu('Navigate', self)
        self._prevFrameAct = navMenu.addAction(
            QIcon(),
            'Previous Frame',
            lambda: self.goToPreviousFrame.emit(),
            QKeySequence(Qt.Key_Left)
        )
        self._nextFrameAct = navMenu.addAction(
            QIcon(),
            'Next Frame',
            lambda: self.goToNextFrame.emit(),
            QKeySequence(Qt.Key_Right)
        )
        navMenu.addAction(
            QIcon(),
            'Jump to Frame',
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