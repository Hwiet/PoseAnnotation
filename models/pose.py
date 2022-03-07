from entities.pose import Pose

import json
import jsonstream
import fastjsonschema
from io import StringIO

from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel


class PoseModel(QStandardItemModel):
    def __init__(self, model: str):
        super().__init__()
        self._items = []

    def setScheme(self, filename):
        fp = open(filename)
        self._validator = fastjsonschema.compile(json.load(fp))
        fp.close()

    def setData(self, io: StringIO) -> int:
        """Sets pose data

        Args:
            io (StringIO): File-like object containing one or more JSON
        documents.

        Returns:
            int: Number of new poses added to the model
        """
        it = jsonstream.load(io)
        new_items = 0
        try:
            while True:
                self._items.append( Pose(next(it), self._validator) )
                new_items += 1
        except StopIteration:
            if new_items == 0:
                raise IndexError(f'{io} is empty.')

        return new_items
