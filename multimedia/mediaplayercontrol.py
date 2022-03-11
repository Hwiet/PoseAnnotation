from PyQt5.QtCore import (
    pyqtSignal,
    pyqtSlot,
    Qt
)

from PyQt5.QtMultimedia import (
    QMediaPlayer
)

class MediaPlayerControl:
    frameChanged = pyqtSlot(int)

    def __init__(self, player):
        """Abstract class for widgets that control a media player, and
        is also controlled by the media player

        Args:
            player (MediaPlayer)
        """
        player.frameCountChanged.connect(self.setRange)
        player.frameChanged.connect(self.setFrame)
        player.videoAvailable.connect(self.isAvailable)
        player.stateChanged.connect(self.onStateChange)

        self.frameChanged.connect(player.setFrame)

    def setEnable(self, enable):
        return NotImplementedError

    @pyqtSlot(int)
    def setFrame(self, frame):
        self.frameChanged.emit(frame)

    @pyqtSlot(int)
    def setRange(self, end):
        return NotImplementedError()

    @pyqtSlot(bool)
    def isAvailable(self, available):
        if not available:
            self.dsiable()

    @pyqtSlot(QMediaPlayer.State)
    def onStateChange(self, state):
        return NotImplementedError