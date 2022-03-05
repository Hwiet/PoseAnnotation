from jsonschema import validate, ValidationError
from typing import Any
from PyQt5.QtGui import QStandardItem


class BaseData:
    def __init__(self, data: dict):
        self._data = data

    def data(self) -> dict:
        """Returns data in object format"""
        return self._data

    def keys(self) -> set:
        return list(self._data.keys())

    def __getitem__(self, key) -> Any:
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

class Joint(BaseData, QStandardItem):
    def __init__(self, data, name: str='name', pos: str='position'):
        super().__init__(data)
        self.name_key = name
        self.pos_key = pos

    @property
    def position(self) -> set:
        return self._data[self.pos_key]

    @position.setter
    def position(self, coords: set) -> None:
        self._data[self.pos_key] = coords

    @property
    def name(self) -> str:
        return self._data[self.name_key]

class Pose(BaseData, QStandardItem):
    def __init__(self, data, schema: dict):
        super().__init__(data)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            raise e
            # del self # self-destruct

        self._joints = [Joint(d) for d in data["joints"]]