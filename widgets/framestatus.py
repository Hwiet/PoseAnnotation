from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QErrorMessage
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QValidator, QIntValidator
from PyQt5.QtMultimedia import (
    QMediaPlayer,
    QMediaContent
)


class FrameStatus(QWidget):
    def __init__(self, player):
        super().__init__()

        self._player = player
        self._lastValidInput = ""

        self._currentWidget = QLineEdit()
        self._currentWidget.setAlignment(Qt.AlignRight)
        self._endWidget = QLabel()

        self._validator = None
        self._error = QErrorMessage(self.parent())

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self._currentWidget)
        self.layout().addWidget(self._endWidget)

        try:
            self.reset(self._player.frameCount(), self._player.frame())
        except:
            self.disable()

        self._player.currentMediaChanged.connect(self.isMediaNotNull)
        self._player.durationChanged.connect(self.checkDuration)
        self._player.stateChanged.connect(self.checkState)
        self._player.positionChanged.connect(self.updateCurrent)

    def disable(self):
        self.disableEditing()
        self.setCurrent('----')
        self.setEnd('----')
    
    def reset(self, end, current=0):
        self.enableEditing()

        self._end = end
        self._validator = QIntValidator(0, end)
        self._currentWidget.setValidator(self._validator)
        
        self.setCurrent(current)
        self.setEnd(end)

        self._currentValue = str(current)
        self._lastValidInput = ""

        self._currentWidget.returnPressed.connect(self.validateInput)

    def setCurrent(self, n):
        self._currentWidget.setText(str(n))

    def setEnd(self, n):
        self._endWidget.setText(f'/{n}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            nextFrame = self._player.frame() + 1
            self._player.setFrame(nextFrame)

            # Key_Up usually moves focus away
            # but we want to keep the focus
            self._currentWidget.setFocus()
            self._currentWidget.selectAll()

        elif event.key() == Qt.Key_Down:
            self._currentWidget.selectAll()
            prevFrame = self._player.frame() - 1
            self._player.setFrame(prevFrame)

            # Key_Down usually moves focus away
            # but we want to keep the focus
            self._currentWidget.setFocus()
            self._currentWidget.selectAll()

    @pyqtSlot()
    def updateCurrent(self):
        self.setCurrent(self._player.frame())
        if self._currentWidget.hasFocus():
            self._currentWidget.selectAll()

    @pyqtSlot(QMediaContent)
    def isMediaNotNull(self, media):
        if media.isNull():
            self.disable()

    @pyqtSlot('qint64')
    def checkDuration(self, duration):
        if duration > 0:
            self.reset(self._player.frameCount(), self._player.frame())

    @pyqtSlot(QMediaPlayer.State)
    def checkState(self, state):
        if state == QMediaPlayer.PlayingState:
            self.disableEditing()
        else:
            self.enableEditing()

    @pyqtSlot()
    def enableEditing(self):
        self._currentWidget.setEnabled(True)

    @pyqtSlot()
    def disableEditing(self):
        self._currentWidget.setEnabled(False)

    @pyqtSlot()
    def validateInput(self):
        lineEdit = self._currentWidget
        lineEdit.selectAll()
        lineEdit.setValidator(self._validator)

        if not lineEdit.hasAcceptableInput():
            self._error.showMessage(f'Your input should be an integer value from 0 to {self._player.frameCount()}')
            lineEdit.setText(self._lastValidInput)
        else:
            self._lastValidInput = lineEdit.text()
            self._player.setFrame(int(lineEdit.text()))

        lineEdit.setValidator(None)