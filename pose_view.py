from joint_item import JointItem


from PyQt5.QtWidgets import QAbstractItemView, QGraphicsView, QGraphicsScene, QGraphicsItemGroup 
from PyQt5.QtCore import QPersistentModelIndex, Qt, pyqtSignal, QVariant


class PoseView(QAbstractItemView):
    def __init__(self):
        super().__init__()

        self._items = list()


    def setModel(self, model):
        for i in range(model.rowCount()):
            index = model.index(i, 1)
            position = model.data(index)
            point = position.value()
            item = JointItem(point.x(), point.y(), 10, 10)
                    
            self._items.append(item)


    @property 
    def items(self):
        return self._items