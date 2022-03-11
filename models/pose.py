from entities.pose import Pose
from . import (
    PoseModelItem,
    PoseItem,
    JointItem
)

import json
import jsonstream
import fastjsonschema
from io import StringIO

from PyQt5.QtCore import (
    Qt,
    QVariant,
    QModelIndex,
    QAbstractItemModel
)


class PoseModel(QAbstractItemModel):
    """A Qt model for reading and storing pose data extracted from an
    image or video.
    """
    def __init__(self, scheme):
        super().__init__()
        self._data = []
        self._modelItems = []
        self._jointLabels = []

        self._setScheme(scheme)

    def _setScheme(self, scheme):
        self._validator = fastjsonschema.compile(scheme)

    def index(self, row, column=0, parent=QModelIndex()) -> QModelIndex:
        parentItem = parent.internalPointer()
        if parentItem is None:
            return self.createIndex(row, column, self._modelItems[row][column])
        return self.createIndex(row, column, parentItem.child(row))

    def parent(self, index) -> QModelIndex:
        if index.isValid():
            parent = index.internalPointer().parent()
            return self.createIndex(index.row(), index.column(), parent)
        return QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        return len(self._modelItems)

    def columnCount(self, parent=QModelIndex()):
        return len(self._modelItems[0])

    def item(self, row, column):
        return self._modelItems[row][column]

    def setItem(self, row, column, item: PoseModelItem):
        """Sets the item for the given row and column to item. The model
        takes ownership of the item. If necessary, the row count and
        column count are increased to fit the item. The previous item at
        the given location (if there was one) is deleted"""
        if len(self._modelItems)-1 < row:
            diff = row+1 - len(self._modelItems)
            self._modelItems.extend( [[]] * diff )
        if len(self._modelItems[row])-1 < column:
            diff = column+1 - len(self._modelItems[row])
            for i in range(diff):
                emptyItem = PoseModelItem()
                emptyItem.row = row
                emptyItem.column = len(self._modelItems[row])
                self._modelItems[row].append(emptyItem)
        item.row = row
        item.column = column
        self._modelItems[row][column] = item

    def setUp(self, stream) -> int:
        """Sets pose data

        Args:
            stream (StringIO): File-like object containing one or more
        JSON documents.

        Returns:
            int: Number of frames or snapshots added.
        """
        # populate data

        poseCount = 0
        jointCount = 0

        self._data.clear()
        it = jsonstream.load(stream)
        new_items = 0
        try:
            while True:
                data = [Pose(obj, self._validator) for obj in next(it)]

                if data != []: # get number used to create model later
                    poseCount = len(data)
                    jointCount = data[0].jointCount()

                self._data.append(data)
                new_items += 1
        except StopIteration:
            pass
        except json.decoder.JSONDecodeError as e:
            self._data.clear()
            raise e

        # set up model items
        for row in range(jointCount+1):
            for column in range(poseCount):
                if row == 0:
                    self.setItem(row, column, PoseModelItem())
                else:
                    self.setItem(row, column, PoseModelItem())

        for i in range(len(self._data)): # 8
            for j in range(poseCount): # 2
                if len(self._data[i]) == 0:
                    self.item(0, j).appendRow(PoseItem(None, self.item(0, j)))
                else:
                    self.item(0, j).appendRow(PoseItem(self._data[i][j], self.item(0, j)))

                # set joint frames
                if len(self._data[i]) == 0:
                    for k in range(jointCount):
                        self.item(k+1, j).appendRow(JointItem(None, self.item(k+1, j)))
                else:
                    for k in range(jointCount):
                        jointDict = self._data[i][j].joint(k)
                        self.item(k+1, j).appendRow(JointItem(jointDict, self.item(k+1, j)))

        return new_items

    def jointCount(self):
        aPose = self._data[self.nextValidFrame()][0]
        return aPose.jointCount()

    def poseCount(self) -> int:
        """The number of detected poses (one for each individual) in the
        image or video."""
        aFrame = self._data[self.nextValidFrame()]
        return len(aFrame)

    def frameCount(self) -> int:
        """The number of frames or snapshots. This is 1 if the data
        originated from an image."""
        return len(self._data)

    def _isValidFrameIndex(self, n) -> bool:
        return 0 <= n < len(self._data)

    def _isImage(self) -> bool:
        return self.frameCount() == 1

    def previousValidFrame(self, n=0):
        if self._isImage():
            return -1
        if not self._isValidFrameIndex(n):
            raise IndexError
            return

        for i in reversed(range(0, n+1)):
            frame = self._data[i]
            if len(frame) > 0: return i
        return -1

    def nextValidFrame(self, n=0) -> int:
        """Return the next frame that contains pose data. This is useful
        for when not every frame has been annotated. If no valid frame
        exists after frame `n`, -1 is returned.

        Args:
            n (int, optional): The frame from which to begin searching.
        Defaults to 0.
        """
        if self._isImage():
            return -1
        if not self._isValidFrameIndex(n):
            raise IndexError
            return

        for i in range(n, len(self._data)):
            frame = self._data[i]
            if len(frame) > 0: return i
        return -1

    def pose(self, person) -> QModelIndex:
        row = 0
        column = person
        return self.createIndex(row, column, self.item(row, column))

    def joint(self, n, person) -> QModelIndex:
        row = n+1
        column = person
        return self.createIndex(row, column, self.item(row, column))

    def frame(self, n, index):
        if index.isValid():
            item = index.internalPointer()
            return self.createIndex(n, 0, item.child(n))
        return QModelIndex()

    def data(self, index, role):
        if index.isValid():
            item = index.internalPointer()
            return item.data(role)
        return None

    def setData(self, index, value, role) -> bool:
        if index.isValid():
            item = index.internalPointer()
            if not item.isValid():
                item.ptr = self._data[item.parent().row][item.parent().column]
            return item.setData(value, role)
        return False

    def jointName(self, index):
        if index.isValid():
            return index.row()-1

    def submit(self):
        s = ''
        for frame in self._data:
            l = []
            for pose in self._data[frame]:
                l.append(pose.data())
            s += json.JSONEncoder().encode(l)