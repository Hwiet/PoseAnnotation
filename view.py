from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt


class View(QGraphicsView):
    def keyPressEvent(self, event):
        key = event.key()
        dz = 1.1

        if key == Qt.Key_0:
            # return to normal zoom level
            self.resetTransform()

        if key == Qt.Key_Minus:
            # zoom out
            self.scale(1/dz, 1/dz)


        if key == Qt.Key_Equal:
            # zoom in
            self.scale(dz, dz)