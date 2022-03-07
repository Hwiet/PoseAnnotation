from entities.pose import Pose

import json
import jsonstream
import fastjsonschema
from io import StringIO

from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class PoseModel(QStandardItemModel):
    """A Qt model for reading and storing pose data extracted from an
    image or video.
    """
    def __init__(self, modelName: str=None, io: StringIO=None):
        super().__init__()
        self._items = []
        self._jointNames = []

        if modelName is not None:
            self.setScheme(f'{modelName}_Pose.json')
        if io is not None:
            self.setUp(io)

    def setScheme(self, scheme):
        self._validator = fastjsonschema.compile(scheme)

    def setJointNames(self, stream):
        """Set joint names.

        model.setJointNames(open('<filename>'), 'r')

        Args:
            stream (StringIO): A text stream.
        """
        for line in stream:
            self._jointNames.append(line.strip())

    def setUp(self, stream) -> int:
        """Sets pose data

        Args:
            stream (StringIO): File-like object containing one or more
        JSON documents.

        Returns:
            int: Number of frames or snapshots added.
        """
        it = jsonstream.load(stream)
        new_items = 0
        try:
            while True:
                self._items.append( [Pose(obj, self._validator) for obj in next(it)] )
                new_items += 1
        except StopIteration:
            pass
        except json.decoder.JSONDecodeError as e:
            self._items.clear()
            raise e

        return new_items

    def jointCount(self):
        aPose = self._items[self.nextValidFrame()][0]
        return aPose.jointCount()

    def poseCount(self) -> int:
        """The number of detected poses (one for each individual) in the
        image or video."""
        aFrame = self._items[self.nextValidFrame()]
        return len(aFrame)

    def frameCount(self) -> int:
        """The number of frames or snapshots. This is 1 if the data
        originated from an image."""
        return len(self._items)

    def _isValidFrameIndex(self, n) -> bool:
        return 0 <= n < len(self._items)

    def _isImage(self) -> bool:
        return self.frameCount() == 1

    def previousValidFrame(self, n=0):
        if self._isImage():
            return -1
        if not self._isValidFrameIndex(n):
            raise IndexError
            return

        for i in reversed(range(0, n+1)):
            frame = self._items[i]
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

        for i in range(n, len(self._items)):
            frame = self._items[i]
            if len(frame) > 0: return i
        return -1

    def pose(self, person) -> QModelIndex:
        return self.createIndex(0, person)

    def joint(self, n, person) -> QModelIndex:
        return self.createIndex(n+1, person)

    def jointName(self, index):
        if index.isValid():
            return self._jointNames[index.row()-1]

    def frameData(self, frame, label, parent):
        if not parent.isValid():
            return QVariant()

        person = parent.column()
        if len(self._items[frame]) == 0:
            # this frame is null
            return QVariant()
        if parent.row() == 0:
            # pose data
            return self._items[frame][person].get(label)
        joint_i = parent.row() - 1
        # joint data
        return self._items[frame][person].joint(joint_i).get(label)