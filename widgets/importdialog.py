from PyQt5.QtCore import (
    Qt,
    pyqtSlot
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
        
        mediaButton = QPushButton('Import media...', self)
        mediaButton.setDefault(True)
        annotationButton = QPushButton('Import annotation...', self)
        self.mediaLabel = QLabel('No media file selected.', self)
        self.annotationLabel = QLabel('No annotation file selected.', self)
        self.mediaFilename = ''
        self.annotationFilename = ''
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
        # buttonBox.accepted.connect(self.submit)
        # buttonBox.rejected.connect(lambda: self.close())

    @pyqtSlot()
    def importMedia(self) -> str:
        self.mediaFilename =  QFileDialog.getOpenFileName(
            parent=self,
            caption='Select media',
            filter='Images (*.png *.jpg);;Videos (*.mp4)'
        )
        self.mediaLabel.setText(self.mediaFilename[0])

    @pyqtSlot()
    def importAnnotation(self) -> str:
        self.annotationFilename = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select annotation',
            filter='Text files (*.txt)'
        )
        self.annotationLabel.setText(self.annotationFilename[0])


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = ImportDialog()
    dialog.show()
    sys.exit(app.exec_())
