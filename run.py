from editor import *
from pose import *
from custom_annotation import CustomFormat
from editor import VideoPoseEditor

from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
import pandas as pd


app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle('Pose Annotation Tool')

keyframes = pd.read_pickle('data/golfDB.pkl').loc[0]['events']
keyframes = [frame - keyframes[0] for frame in keyframes]
keyframes.pop(0)
keyframes.pop(len(keyframes) - 1)

annotation = CustomFormat('data/annotation/Golf Swing 0.txt')
media = AnnotatedVideo('data/media/Golf Swing 0.mp4', annotation, keyframes)

video_editor = VideoPoseEditor(media)
widget = video_editor.get_widget()

window.setCentralWidget(widget)
window.show()

sys.exit(app.exec_())