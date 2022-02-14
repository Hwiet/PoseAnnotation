from custom_annotation import CustomFormat
from annotated_media import AnnotatedVideo
from pose_model import PoseModel


import sys
import unittest
import pandas as pd
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QVariant, QPointF, QModelIndex, QMetaType


class PoseModelTest(unittest.TestCase):
    def setUp(self):
        app = QApplication(sys.argv)

        keyframes = pd.read_pickle('data/golfDB.pkl').loc[0]['events']
        keyframes = [frame - keyframes[0] for frame in keyframes]
        keyframes.pop(0)
        keyframes.pop(len(keyframes) - 1)

        media = AnnotatedVideo('data/media/Golf Swing 0.mp4', CustomFormat('data/annotation/Golf Swing 0.txt'), keyframes)

        self.pose_model = PoseModel(media.poses[0])


    def test_index(self):
        index1 = self.pose_model.index(0, 0)
        index2 = self.pose_model.index(0, 1)

        self.assertEqual(QMetaType.QString, self.pose_model.data(index1).type())
        self.assertEqual(QMetaType.QPointF, self.pose_model.data(index2).type())
