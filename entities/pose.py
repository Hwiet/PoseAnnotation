import fastjsonschema
from fastjsonschema import JsonSchemaException
from typing import Any
import json
from PyQt5.QtGui import QStandardItem
from functools import cached_property
from copy import deepcopy


class BaseData():
    def __init__(self):
        self._data = {}

    def data(self) -> dict:
        return self._data

    def keys(self) -> set:
        return list(self._data.keys())

    def get(self, key) -> Any:
        return self._data[key]

    def __getitem__(self, key) -> Any:
        return self.get(key)

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

class Pose(BaseData):
    def isNull(self) -> bool:
        """A pose is null if it has no joints"""
        return "joints" in self._data

    def jointCount(self) -> int:
        return len(self["joints"])

    def joint(self, n):
        return self["joints"][n]

    def setJoints(self, obj):
        """Extract joint data from pose object""" 
        self['joints'] = [d for d in obj['joints'] if isinstance(d, dict)]
        self['joints'].sort(key=lambda o: o['name'])

    def __init__(self, data_=None, validate=None):
        """A wrapper for a dictionary, where the data of interest is
        the list `self._data["joints"]`. 

        Args:
            data (object): Object representation of the pose that must
        be validated.
            validate (function): Validation function generated with
        `fastjsonschema.compile(<schema>)`

        Raises:
            JsonSchemaException: `data` is not valid.
        """
        super().__init__()
        if data_ is None:
            return # create null pose
        try:
            validate(data_)
            self.setJoints(data_)
            
            # set other attributes
            keys = list(data_.keys())
            keys.remove('joints')
            for key in keys:
                self[key] = data_[key]

        except JsonSchemaException as e:
            raise e
            del self # self-destruct