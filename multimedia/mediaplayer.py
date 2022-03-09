import cv2
from math import floor, ceil
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal


class MediaPlayer(QMediaPlayer):
    DEFAULT_NOTIFY_INTERVAL = 10

    frameChanged = pyqtSignal(int)
    frameCountChanged = pyqtSignal(int)

    def __init__(self, filename):
        super().__init__()

        super().setMedia(QMediaContent(QUrl(filename)))
        self._fps = cv2.VideoCapture(filename).get(cv2.CAP_PROP_FPS)
        self.frameCountChanged.emit(self._millisecondsToFrames(self.duration()))

    @property
    def fps(self):
        return self._fps

    def play(self):
        super().play()
        self.setNotifyInterval(floor(1000 / self._fps))

    def pause(self):
        super().pause()
        self.setNotifyInterval(self.DEFAULT_NOTIFY_INTERVAL)

    def stop(self):
        super().stop()
        self.setNotifyInterval(self.DEFAULT_NOTIFY_INTERVAL)

    def setVideoOutput(self, surface):
        super().setVideoOutput(surface)
        self.setPosition(0)
        self.pause()

    def frame(self):
        return self._millisecondsToFrames(self.position())

    def frameCount(self):
        return self._millisecondsToFrames(self.duration())

    def setFrame(self, n):
        target = self._framesToMilliseconds(n)
        if 0 <= target < self.duration():
            # setting state to `play` before changing position
            # removes black flashes in between rapid position changes
            self.play()
            self.setPosition(target)
            self.pause()
            self.frameChanged.emit(n)

    def _framesToMilliseconds(self, f):
        return ceil(f * 1000 / self._fps)

    def _millisecondsToFrames(self, m):
        return floor(m / 1000 * self._fps)