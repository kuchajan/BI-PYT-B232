"""Implements an enum class to represent user actions in level"""
from enum import Enum


class Action(Enum):
    """Enum that represent user actions"""
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    RESET = 4
    EXIT = 5
