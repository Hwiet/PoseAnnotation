from editor import *
from pose import *
from custom_annotation import CustomFormat

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import json
import pandas as pd

annotation = CustomFormat('data/sample.txt')
media = AnnotatedImage('data/frame10.jpg', annotation)
app = QApplication(sys.argv)
ex = ImagePoseEditor(media)
sys.exit(app.exec_())