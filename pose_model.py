from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex, QVariant, QPointF
from PyQt5.QtGui import QStandardItemModel

from pose import Pose


class JointItem:
    def __init__(self, name, position):
        self._name = name
        self._position = position


    @property
    def name(self):
        return QVariant(self._name)


    @property
    def position(self):
        return QVariant(QPointF(*self._position))


    def data(self, column):
        return {
            0: self.name,
            1: self.position
        }[column]


class PoseModel(QAbstractItemModel):
    def __init__(self, pose):
        super().__init__()

        self.joints = list()
        self.setUp(pose)


    def setUp(self, pose):
        for i, (_, joint) in enumerate(pose.joints.items()):
            self.joints.append(JointItem(str(joint.name), joint.position))


    def index(self, row, column, parent=QModelIndex()):
        if parent != QModelIndex():
            return QModelIndex()

        item = self.joints[row]

        if column == 0:
            return self.createIndex(row, column, item.name)
        elif column == 1:
            return self.createIndex(row, column, item.position)

        return QModelIndex()


    def parent(self, index):
        return QModelIndex()


    def rowCount(self):
        return len(self.joints)


    def columnCount(self, parent):
        return QModelIndex()


    def data(self, index: QModelIndex):
        if not index.isValid():
            return QVariant()

        item = self.joints[index.row()]
        return item.data(index.column())