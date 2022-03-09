from PyQt5.QtWidgets import QWidget


class KeyHoldWidget(QWidget):
    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if hasattr(self, '__delay')


    def keyHoldEvent(self, event):
        pass


    def keyAutoRepeatDelay(self):
        pass

    
    def keyAuto