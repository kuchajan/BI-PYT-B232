"""Implements an enum class to represent user actions in level"""
from enum import Enum


class Action(Enum):
    """Enum that represent user actions"""
    NOTHING = 0
    MOVE_UP = 1
    MOVE_RIGHT = 2
    MOVE_DOWN = 3
    MOVE_LEFT = 4
    ENTER = 5
    RESET = 6
    EXIT = 7

    def __eq__(self, other):
        return isinstance(other, Action) and other.value == self.value
