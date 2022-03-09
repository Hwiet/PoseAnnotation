from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # graphics.setJointModels(jointModels)
        # self.setCentralWidget(graphics)

        # frameCount = player.frameCount()

        # progressbar = VideoProgressToolBar(self)
        # self.addToolBar(Qt.BottomToolBarArea, progressbar)
        # slotSignalPairs.append(SlotSignalPair(signal=progressbar.widget.valueChanged, slot=graphics.showFrame))
        # slotSignalPairs.append(SlotSignalPair(signal=player.frameCountChanged, slot=progressbar.widget.setRange))


        # player.positionChanged.connect(self.menuBar().onPositionChange)


# model = PoseModel('PoseNet', jsonstream.load('data/annotation/Golf Swing 0.txt'))
# model.setJointNames('schema/PoseNet_Joints')

# player = MediaPlayer()
# graphics = GraphicsView('data/media/Golf Swing 0.mp4', player)



# for ss in slotSignalPairs:
#     graphics.registerSS(ss)