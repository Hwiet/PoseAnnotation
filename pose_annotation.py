import sys
import json
from os.path import abspath, dirname

from widgets import (
    MainWindow,
    MenuBar,
    StatusBar,
    FrameStatus,
    VideoProgressToolBar,
    ImportDialog
)

from models import (
    PoseModel
)

from graphics import PoseView
from multimedia import MediaPlayer

from PyQt5.QtWidgets import QApplication  

from PyQt5.QtCore import (
    Qt,
    QSettings
)

class App(QApplication):
    pass

if __name__ == '__main__':
    def import_(mediaFilename, annotationFilename):
        settings.beginGroup("Files");
        settings.setValue("Media directory", dirname(abspath(mediaFilename)))
        settings.setValue("Annotation directory", dirname(abspath(annotationFilename)))

        # TODO allow selection of supported models by the user, and not
        # hardcode model
        with open("supported_models/PoseNet/schema.json") as fp:
            scheme = json.load(fp)

        with open("supported_models/PoseNet/constants.json") as fp:
            constants = json.load(fp)
            keypoints = constants["keypoints"]
            chain = constants["pose_chain"]

        model = PoseModel(scheme)

        with open(annotationFilename) as fp:
            model.setUp(fp)

        poseview = PoseView(model, keypoints, chain)
        mediaplayer = MediaPlayer(mediaFilename)

        for item in poseview.items():
            mediaplayer.frameChanged.connect(item.setFrame)
            menubar.toggleLabels.connect(item.toggleLabel)

        mediaplayer.setVideoOutput(poseview.videoItem())

        menubar.save.connect(model.submit)
        menubar.revert.connect(model.revert)

        menubar.zoomIn.connect(poseview.zoomIn)
        menubar.zoomOut.connect(poseview.zoomOut)
        menubar.fitOnScreen.connect(poseview.fitInView)

        menubar.goToPreviousFrame.connect(lambda: mediaplayer.setFrame(mediaplayer.frame()-1))
        menubar.goToNextFrame.connect(lambda: mediaplayer.setFrame(mediaplayer.frame()+1))
        menubar.goToFrame.connect(mediaplayer.setFrame)

        window.setCentralWidget(poseview)


    app = App(sys.argv)
    app.setOrganizationName('MyCompany')
    app.setApplicationName('Pose Annotation')
    settings = QSettings()

    window = MainWindow()
    menubar = MenuBar()
    statusbar = StatusBar() 

    window.setMenuBar(menubar)
    window.setStatusBar(statusbar)

    # TODO make these live in an EditorTab
    mediaFilename = ''
    annotationFilename = ''
    scheme = None
    constants = None
    keypoints = None
    chain = None
    model = None
    poseview = None
    mediaplayer = None
    framestatus = None
    def getFiles():
        dialog = ImportDialog()
        dialog.open(lambda: import_(dialog.mediaFilename(), dialog.annotationFilename()))

    menubar.import_.connect(getFiles)

    window.showMaximized()
    sys.exit(app.exec_())