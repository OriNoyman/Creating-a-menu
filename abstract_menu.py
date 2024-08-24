from abc import ABC, abstractmethod
from typing import Callable

class MenuItem(ABC):
    def __init__ (self, name : str):
        self.name = name
    
    @abstractmethod
    def execute(self):
        pass

class ActionMenuItem(MenuItem):
    def __init__(self, name : str, action : Callable):
        super().__init__(name)
        self._action = action

    def execute(self):
        self._action()    