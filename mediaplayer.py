import cv2
from math import floor, ceil
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, pyqtSlot


class MediaPlayer(QMediaPlayer):
    DEFAULT_NOTIFY_INTERVAL = 1000


    def __init__(self):
        super().__init__()
        self._fps = 0


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


    def setMedia(self, filename):
        super().setMedia(QMediaContent(QUrl(filename)))

        self._fps = cv2.VideoCapture(filename).get(cv2.CAP_PROP_FPS)


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

    
    def _framesToMilliseconds(self, f):
        return ceil(f * 1000 / self._fps)


    def _millisecondsToFrames(self, m):
        return floor(m / 1000 * self._fps)