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
        self._data += [None] * 2
        
        # data 0 is always the position
        self._data[0] = position

        # data 1 is always the joint's label
        self._data[1] = name


    @property
    def pose(self):
        return self._pose


    @property
    def position(self):
        return QVariant(QPointF(*self._data[0]))


    @position.setter
    def position(self, pos):
        self._data[0] = pos


    @property
    def name(self):
        return QVariant(self._data[1])


    def data(self, n):
        try:
            if n == 0:
                return self.position

            return self._data[n]
        except IndexError:
            print("Attempted to reach out of bounds joint data", file=sys.stderr)
        return None


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


    def joint(self, n):
        try:
            return self._joints[b]
        except IndexError:
            print("Joint index out of range", file=sys.stderr)


    def data(self, n):
        try:
            return self._data[n]
        except IndexError:
            print("Attempted to reach out of bounds pose data", file=sys.stderr)
        return None


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
                continue

            joints = list()

            for j, (_, joint) in enumerate(pose.joints.items()):
                joints.append(JointItem(str(joint.name), joint.position, pose, j))

            self._poses.append(PoseItem(joints, i))
            i += 1
            

    def index(self, row, column, parent=QModelIndex()):
        if not parent.isValid():
            data = self._poses[row].data(column)
            return self.createIndex(row, column, data)
        else:
            # returns reference to the item
            # this will always be a PoseItem
            parent_item = parent.internalPointer()

        try:
            item = parent_item.joint(row)
            data = item.data(column)
            return self.createIndex(row, column, data)
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
        if not parent.isValid():
            return 0

        if parent == QModelIndex():
            return len(self._poses)
    
        parent_item = parent.internalPointer() 
        return parent_item.rowCount()


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
        return item.data(item.column())


    def setData(self, index, value, role):
        if not index.isValid():
            return false

        data = index.internalPointer()
        data = value
        return true


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        else:
            return index.internalPointer().flags()