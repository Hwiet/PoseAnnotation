from PyQt5.QtCore import (
    Qt,
    QModelIndex,
    QVariant,
    QPointF
)

class PoseModelItem():
    def __init__(self, ptr=None, parent: 'PoseModelItem'=None):
        """
        Args:
            ptr: Reference to data
        """
        super().__init__()
        self._parent = parent
        self._items = []
        if ptr is not None:
            self.ptr = ptr
            self._keys = list(ptr.keys())

    def isValid(self) -> bool:
        return hasattr(self, 'ptr') and self.ptr is not None

    def parent(self):
        return self._parent

    @property
    def row(self):
        if self._parent is None:
            return -1
        return self._row

    @row.setter
    def row(self, n):
        self._row = n

    @property
    def column(self):
        if self._parent is None:
            return -1
        return self._column

    @row.setter
    def column(self, n):
        self._column = n

    def appendRow(self, item):
        item.row = len(self._items)
        item.column = 0
        self._items.append([item])

    def child(self, row, column=0):
        if self._items != []:
            return self._items[row][column]
        return None

    def data(self, role):
        if not self.isValid():
            return None
        if isinstance(role, str):
            if role == 'position':
                return QPointF(*self.ptr[role])
            return self.ptr[role]
        if isinstance(role, int) and role >= Qt.UserRole+1:
            if self._keys[role] in self.ptr:
                return self.ptr[self._keys[role]]
            else:
                return None
        return None

    def setData(self, value, role):
        if isinstance(role, str):
            if role == 'position':
                self.ptr[role] = value.toPointF()
            else:
                self.ptr[role] = value
            return True
        if isinstance(role, int) and role >= Qt.UserRole+1:
            if self._keys[role] in self.ptr:
                self.ptr[self._keys[role]] = value
                return True
            else:
                return False
        return False

    def rowCount(self):
        return len(self._items)

class PoseItem(PoseModelItem):
    pass

class JointItem(PoseModelItem):
    def __init__(self, ptr, parent):
        super().__init__(ptr, parent)
        if ptr is not None:
            # position needs to be at front of list
            self._keys.remove('position')
            self._keys.insert(0, 'position')