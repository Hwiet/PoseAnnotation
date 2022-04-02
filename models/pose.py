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
import tempfile
import python_jsonschema_objects as pjs

from PyQt5.QtCore import (
    pyqtSlot,
    Qt,
    QVariant,
    QModelIndex,
    QAbstractItemModel
)

from PyQt5.QtGui import QStandardItemModel, QStandardItem

class PoseModel(QStandardItemModel):
    """A Qt model for reading and storing pose data extracted from an
    image or video.
    """
    _poseCls = None
    _jointCls = None
    _jointCount = 17
    
    def __init__(self, scheme):
        super().__init__()
        self._setScheme(scheme)

    def _setScheme(self, scheme):
        builder = pjs.ObjectBuilder(json.load(scheme)) # pass in both pose scheme and joint scheme
        ns = builder.build_classes(standardize_names=False, named_only=True)
        self._poseCls = ns.PoseNetPose
        self._jointCls = ns.Joint

    def setUp(self, stream) -> int:
        it = jsonstream.load(stream)

        try:
            currFrame = -1
            emptyFrames = [] # indices
            while True:
                poses = next(it)
                currFrame += 1

                if poses == []:
                    # if self.rowCount() == 0:
                    #     emptyFrames.append(currFrame)
                    continue

                # if len(emptyFrames) > 0:
                #     for i in range(self.rowCount()):
                #         for j in range(self.columnCount()):
                #             for k in emptyFrames:
                #                 self.item(i, j).setChild(k, QStandardItem())

                column = 0 # columns = poses
                for p in poses:
                    pose = self._poseCls(**p)

                    # clear out integers in list of joints
                    pose.joints = [i for i in pose.joints if type(i) is dict]

                    # sort the joints by their index
                    pose.joints = sorted(pose.joints, key=lambda a: a['name'])

                    row = 0
                    for j in pose.joints:
                        currItem = self.item(row, column)

                        if currItem is None:
                            self.setItem(row, column, QStandardItem())
                            currItem = self.item(row, column)

                        currItem.setData(j['name'], Qt.DisplayRole)

                        currChild = currItem.child(currFrame)
                        if currChild is None:
                            currItem.setChild(currFrame, QStandardItem())
                            currChild = currItem.child(currFrame)

                        currChild.setData(j, Qt.UserRole+1)
                        currChild.setData(pose, Qt.UserRole+2)
                        row += 1

                    column += 1                    
        except StopIteration:
            # for i in range(self.columnCount()):
            #     self.sort(i)

            # print(self.itemData(self.index(3, 0, self.index(15, 0))))
            print(self.item(15).child(3).data())
            # joint 0 for 
            # index = self.index(3, 0, self.index(15, 0))
            # print(index.isValid())
            
            # data = index.internalPointer.data()
            # print(data)
    # def frameCount(self):
    #     return self.rowCount()

    # def poseCount(self):
    #     return self.columnCount()

    # def getPosition(self, row, column):
    #     self.item(row, column).data().

    # def previousValidFrame(self, n=0):
    #     if self.rowCount() == 1:
    #         return -1

    #     if 0 <= n < self.rowCount(): 
    #         for i in reversed(range(0, n+1)):
    #             if self.itemData()
    #             frame = self._data[i]
    #             if len(frame) > 0: return i
    #     return -1 


    # def nextValidFrame(self, n=0) -> int:
    #     """Return the next frame that contains pose data. This is useful
    #     for when not every frame has been annotated. If no valid frame
    #     exists after frame `n`, -1 is returned.

    #     Args:
    #         n (int, optional): The frame from which to begin searching.
    #     Defaults to 0.
    #     """
    #     if self._isImage():
    #         return -1
    #     if not self._isValidFrameIndex(n):
    #         raise IndexError
    #         return

    #     for i in range(n, len(self._data)):
    #         frame = self._data[i]
    #         if len(frame) > 0: return i
    #     return -1

    # def _isEmptyItem(self, row, column):
    #     return not self.data()