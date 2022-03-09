from PyQt5.QtCore import QObject
from PyQt5.QtCore import QPointF
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGraphicsItem
from functools import partial
from typing import Dict, List   


class Controller(QObject):
    """A singleton object to implement event listeners for QGraphicsItems.
    QGraphicsItem does not inherit from QObject, so they could not use Qt's
    signals and slots mechanism.
    
    Events are designated a name given as a string, for example
    'positionChanged'."""
    __instance = None
    __signal: Dict[str, List[partial]] = None

    @staticmethod
    def getInstance():
        if Controller.__instance is None:
            Controller()
        return Controller.__instance

    def __init__(self):
        if Controller.__instance is None:
            Controller.__instance = self
            Controller.__signal = dict()
        else:
            raise Exception(f'Cannot create another instance of a singleton class {self.__name__}')

    def registerListener(self, name: str, functor):
        """Adds a functor to fire when event with name `name` is emitted. If
        there is no event with the name, it is created.
        
        Arguments:
        name -- Name of the event
        functor -- Function to call when event is emitted.
        """
        if not Controller.__signal.__contains__(name):
            Controller.__signal[name] = list()
        Controller.__signal[name].append(functor)

    def removeListener(self, name: str, functor):
        """Deregisters functor from an event."""
        Controller.__signal[name].remove(functor)

    def fire(self, name: str, *args):
        """Emit the event with the name `name`. args are passed to the functors
        registered under the event.
        
        Arguments:
        name -- Name of the event to fire
        args -- Arguments that will be passed to all functors registered to the
        event"""
        for p in Controller.__signal[name]:
            p = partial(p, *args)
            p()


class ControlledItem(QGraphicsItem):
    """Abstract class of QGraphicsItem that enables the item to register
    events."""
    def addListener(self, name: str, functor):
        Controller.getInstance().registerListener(name, functor)

    def removeListener(self, name: str, functor):
        Controller.getInstance().removeListener(name, functor)

    def emit(self, name, *args):
        Controller.getInstance().fire(name, *args)