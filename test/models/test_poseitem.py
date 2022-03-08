import unittest
from mock import MagicMock
from models.poseitem import PoseModelItem


class TestPoseModelItem(unittest.TestCase):
    def test_insert_row(self):
        item = PoseModelItem()
        item.appendRow(MagicMock())
        item.appendRow(MagicMock())
        self.assertEqual(item.rowCount(), 2)

    def test_child(self):
        item = PoseModelItem()
        child_item = MagicMock()
        item.appendRow(MagicMock())
        item.appendRow(child_item)
        self.assertEqual(item.child(1), child_item)