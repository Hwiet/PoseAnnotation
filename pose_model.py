import sys

from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QPersistentModelIndex, QVariant, QPointF
from PyQt5.QtGui import QStandardItemModel

from pose import Pose


class PoseModelItem:
    def __init__(self, index):
        self._data = list()
        self._index = index


    @property
    def index(self):
        return self._index


    def columnCount(self):
        return len(self._data)


    def data(self, n):
        return NotImplementedError


class JointItem(PoseModelItem):
    def __init__(self, name, position, pose, index):
        super().__init__(index)

        self._pose = pose

        self._data.insert(0, index)
        self._data.insert(1, QVariant(QPointF(*position)))
        self._data.insert(2, QVariant(name))


    @property
    def pose(self):
        return self._pose


    @property
    def name(self):
        return QVariant(self._data[1])


    def setData(self, n, data):
        try:
            self._data[n] = data
        except:
            return False
        return True


    def data(self, n):
        return self._data[n]


    def rowCount(self):
        return 0


    def flags(self):
        return Qt.ItemIsSelectable \
            & Qt.ItemIsEditable \
            & Qt.ItemIsDragEnabled \
            & Qt.ItemIsEnabled \
            & Qt.ItemNeverHasChildren


class PoseItem(PoseModelItem):
    def __init__(self, joints, index):
        super().__init__(index)

        self._joints = joints
        self._data.insert(0, index)


    def joint(self, n):
        return self._joints[n]


    def data(self, n):
        return self._data[n]


    def rowCount(self):
        return len(self._joints)


    def flags(self):
        return Qt.ItemIsEditable


class PoseModel(QAbstractItemModel):
    """
    Attributes:
        poses (list[PoseItem]): List of pose data per frame. Element 0 = Frame 0.
    """
    def __init__(self, poses):
        super().__init__()

        self._poses = list()
        self.setUp(poses)


    def setUp(self, poses):
        i = 0
        for pose in poses:
            if pose is None:
                self._poses.append(PoseItem(list(), i))
            else:
                joints = list()

                for j, (_, joint) in enumerate(pose.joints.items()):
                    joints.append(JointItem(str(joint.name), joint.position, pose, j))

                self._poses.append(PoseItem(joints, i))
                
            i += 1
        return

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            data = self._poses[row].data(column)
            return self.createIndex(row, column, self._poses[row])
        else:
            # returns reference to the item
            # this will always be a PoseItem
            parent_item = parent.internalPointer()

        try:
            item = parent_item.joint(row)
            data = item.data(column)
            return self.createIndex(row, column, item)
        except:
            # return empty index
            return QModelIndex()


    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()

        if type(child_item) is JointItem:
            return self.self.createIndex(child_item.index, 0, child_item.pose)
        else:
            return QModelIndex
           
    
    def rowCount(self, parent=QModelIndex()):
        if parent == QModelIndex():
            # return row count of the model
            return len(self._poses)

        dsaf = self.index(0, 0, parent)

        parent_item = parent.internalPointer() 
        
        if parent_item is not None:
            return parent_item.rowCount()
        else:
            return len(self._poses)


    def columnCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return 0

        if parent == QModelIndex():
            return 1

        parent_item = parent.internalPointer() 
        return parent_item.columnCount()


    def data(self, index):
        if not index.isValid(): 
            return QVariant()

        item = index.internalPointer()
        return item.data(index.column())


    def setData(self, index, value):
        if not index.isValid():
            return False

        item = index.internalPointer()
        item.setData(index.column(), value)
        return True


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        else:
            return index.internalPointer().flags()