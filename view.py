from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, pyqtSignal


class View(QGraphicsView):
    toPrevFrame = pyqtSignal()
    toNextFrame = pyqtSignal()


    def keyPressEvent(self, event):
        key = event.key()
        dz = 1.1


        if key == Qt.Key_Left:
            self.toPrevFrame.emit()


        elif key == Qt.Key_Right:
            self.toNextFrame.emit()


        elif key == Qt.Key_0:
            # return to normal zoom level
            self.resetTransform()


        elif key == Qt.Key_Minus:
            # zoom out
            self.scale(1/dz, 1/dz)


        elif key == Qt.Key_Equal:
            # zoom in
            self.scale(dz, dz)