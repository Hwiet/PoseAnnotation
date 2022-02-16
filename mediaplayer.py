import cv2
from math import ceil
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class MediaPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self._fps = None

        self.mediaStatusChanged.connect(self.buffered)


    def buffered(self):
        if self.mediaStatus() == 3: print('loaded')


    @property
    def fps(self):
        return self._fps


    def setMedia(self, filename):
        super().setMedia(QMediaContent(QUrl(filename)))

        self._fps = cv2.VideoCapture(filename).get(cv2.CAP_PROP_FPS)


    def frame(self):
        return self.position() / self._fps


    def setFrame(self, n):
        target = ceil(n * self._fps)
        if target < self.duration():
            self.setPosition(target)