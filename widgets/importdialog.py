from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    pyqtSlot,
    QSettings
)
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QPushButton,
    QGridLayout,
    QWidgetItem,
    QLabel,
    QDialogButtonBox
)

class ImportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('MyCompany', 'Pose Annotation')
        
        mediaButton = QPushButton('Import media...', self)
        mediaButton.setDefault(True)
        annotationButton = QPushButton('Import annotation...', self)
        self.mediaLabel = QLabel('No media file selected.', self)
        self.annotationLabel = QLabel('No annotation file selected.', self)
        self._mediaFilename = ''
        self._annotationFilename = ''
        buttonBox = QDialogButtonBox( QDialogButtonBox.Cancel | QDialogButtonBox.Ok, Qt.Horizontal, self )

        self.setLayout( QGridLayout() )
        self.setModal(True)

        self.layout().addItem( QWidgetItem(mediaButton), 0, 0, )
        self.layout().addItem( QWidgetItem(annotationButton), 1, 0 )
        self.layout().addItem( QWidgetItem(self.mediaLabel), 0, 1 )
        self.layout().addItem( QWidgetItem(self.annotationLabel), 1, 1 )
        self.layout().addItem( QWidgetItem(buttonBox),  2, 0 )

        mediaButton.clicked.connect(self.importMedia)
        annotationButton.clicked.connect(self.importAnnotation)

        buttonBox.accepted.connect(self.accepted)
        buttonBox.rejected.connect(self.rejected)

        self.accepted.connect(self.close)
        self.rejected.connect(self.close)

    def open(self, handler):
        self.accepted.connect(handler)
        super().open()

    @pyqtSlot()
    def importMedia(self) -> str:
        self._mediaFilename =  QFileDialog.getOpenFileName(
            parent=self,
            directory=self.settings.value('Files/Media directory'),
            caption='Select media',
            filter='Videos (*.mp4);;Images (*.png *.jpg)'
        )[0]
        self.mediaLabel.setText(self._mediaFilename)

    @pyqtSlot()
    def importAnnotation(self) -> str:
        self._annotationFilename = QFileDialog.getOpenFileName(
            parent=self,
            directory=self.settings.value('Files/Annotation directory'),
            caption='Select annotation',
            filter='Text files (*.txt)'
        )[0]
        self.annotationLabel.setText(self._annotationFilename)

    def mediaFilename(self) -> str:
        return self._mediaFilename

    def annotationFilename(self) -> str:
        return self._annotationFilename

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ImportDialog()
    dialog.show()
    sys.exit(app.exec_())
