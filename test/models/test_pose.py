from models.pose import PoseModel

import sys
import unittest
from PyQt5.QtWidgets import QApplication
from io import StringIO
import jsonstream


class TestPoseModel(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.model = PoseModel()
        self.model.setScheme({
            "type": "object",
            "properties": {
                "joints": {
                    "type": "array",
                    "items": { "$ref": "#/$defs/joint" }
                },
                "confidence": { "type": "number" }
            },
                "required": [ "joints", "confidence" ],
            "$defs": {
                "joint": {
                    "type": "object",
                    "properties": {
                        "name": { "type": "integer" },
                        "position": { "type": "array", "items": { "type": "number" }, "minItems": 2 }
                    },
                    "required": [ "name", "position" ]
                }
            }
        })
        self.model.setJointNames(StringIO('left wrist\nright wrist'))
        self.model.setUp(StringIO("""
            []
            []
            []
            [
                {
                    "joints": [
                        {
                            "name": 0,
                            "position": [
                                695.5750487329434,
                                219.26809210526315
                            ]
                        },
                        {
                            "name": 1,
                            "position": [
                                618.78167641325535,
                                342.70833333333331
                            ]
                        }
                    ],
                    "confidence": 0.34125325115
                }
            ]
            []
            []
            []
            [
                {
                    "joints": [
                        {
                            "name": 0,
                            "position": [
                                654.99025341130596,
                                442.94407894736838
                            ]
                        },
                        {
                            "name": 1,
                            "position": [
                                632.11500974658861,
                                404.00202165570175
                            ]
                        }
                    ],
                    "confidence": 0.98643800
                }
            ]"""))

    def test_set_up_success_null(self):
        model = PoseModel()
        io = StringIO("[]")
        self.assertEqual(model.setUp(io), 1)

    def test_frame_count(self):
        self.assertEqual(self.model.frameCount(), 8)

    def test_joint_count(self):
        self.assertEqual(self.model.jointCount(), 2)

    def test_pose_count(self):
        self.assertEqual(self.model.poseCount(), 1)

    def test_prev_valid_frame_success(self):
        self.assertEqual(
            self.model.previousValidFrame(6),
            3
        )
        self.assertEqual(
            self.model.previousValidFrame(self.model.frameCount()-1),
            self.model.frameCount()-1
        )
        self.assertEqual(
            self.model.previousValidFrame(0),
            -1
        )

    def test_prev_valid_frame_fail(self):
        with self.assertRaises(IndexError):
            self.model.previousValidFrame(-1)
            self.model.previousValidFrame(self.model.frameCount())

    def test_next_valid_frame(self):
        self.assertEqual(self.model.nextValidFrame(), 3)

    def test_pose_data(self):
        index = self.model.pose(0)
        self.assertAlmostEqual(
            self.model.frameData(3, 'confidence', index),
            0.34125325115
        )

    def test_joint_data(self):
        index = self.model.joint(0, 0)
        self.assertEqual(
            self.model.frameData(3, 'name', index), 0)

    def test_joint_name(self):
        index = self.model.joint(0, 0)
        self.assertEqual('left wrist', self.model.jointName(index))