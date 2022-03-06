import fastjsonschema
from fastjsonschema import JsonSchemaException
from typing import Any
from PyQt5.QtGui import QStandardItem
from functools import cached_property


class BaseData:
    def __init__(self):
        self._data = {}

    def keys(self) -> set:
        return list(self._data.keys())

    def __getitem__(self, key) -> Any:
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

class Joint(BaseData, QStandardItem):
    def __init__(self, data_):
        super().__init__()
        try:
            self.validate(data_)
        except JsonSchemaException as e:
            raise e

    @cached_property
    def validate(self):
        """Check that joint data contains at least a name and position
        attribute"""
        return fastjsonschema.compile({
            "type": "object",
            "properties": {
                "name": { "type": "integer" },
                "position": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    },
                    "minItems": 2
                }
            },
            "required": [ "name", "position" ]
        })

class Pose(BaseData, QStandardItem):
    def isNull(self) -> bool:
        """A pose is null if it has no joints"""
        return "joints" in self._data

    def setJoints(self, obj):
        """Extract joint data from pose object""" 
        self["joints"] = [Joint(d) for d in obj['joints'] if isinstance(d, dict)]

    def __init__(self, data_, validate):
        """A wrapper for a dictionary, where the data of interest is
        the list `self._data["joints"]`. 

        Args:
            data (object): Object representation of the pose that must
        be validated. If data is `[]`, a null pose is created.
            validate (function): Validation function generated with
        `fastjsonschema.compile(<schema>)`

        Raises:
            JsonSchemaException: `data` is not valid.
        """
        super().__init__()
        if isinstance(data_, list):
            if len(data_) == 0:
                return # create null pose
            data_ = data_[0]

        try:
            validate(data_)
            self.setJoints(data_)
        except JsonSchemaException as e:
            raise e
            del self # self-destruct