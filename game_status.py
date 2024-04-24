"""Class that represents the current game status, such as the player position and positions of boxes"""

import numpy as np

import constants as Const
from action import Action

class GameStatus:
    """Class that represents the current game status, such as the player position and positions of boxes"""
    def __init__(self, player_pos: np.array, box_pos: set):
        self.player_pos = player_pos
        self.box_pos = frozenset(box_pos)

    def copy(self):
        """Creates a copy of the instance"""
        return GameStatus(self.player_pos, self.box_pos)

    def handle_action(self, action: Action, matrix: np.array):
        """Handles a move action"""
        move_vec = np.zeros((2), np.int8)
        if action == action.MOVE_UP:
            # y--
            move_vec[1] -= 1
        elif action == action.MOVE_RIGHT:
            # x++
            move_vec[0] += 1
        elif action == action.MOVE_DOWN:
            # y++
            move_vec[1] += 1
        elif action == action.MOVE_LEFT:
            # x--
            move_vec[0] -= 1
        else:
            # invalid action
            return self.copy()

        new_pos = self.player_pos + move_vec
        if matrix[new_pos[0]][new_pos[1]] == Const.WALL: # attempted to move into a wall
            return self.copy()

        if tuple(new_pos) not in self.box_pos:
            return GameStatus(new_pos, self.box_pos)

        # there's a box
        new_single_box_pos = new_pos + move_vec
        if matrix[new_single_box_pos[0]][new_single_box_pos[1]] == Const.WALL or tuple(new_single_box_pos) in self.box_pos:
            # moving box into wall or into box
            return self.copy()

        new_box_pos = set(self.box_pos)
        new_box_pos.remove(tuple(new_pos))
        new_box_pos.add(tuple(new_single_box_pos))
        return GameStatus(new_pos, new_box_pos)

    def __hash__(self) -> int:
        return hash((tuple(self.player_pos), self.box_pos))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GameStatus) and np.array_equal(self.player_pos, other.player_pos) and self.box_pos == other.box_pos

    def __ne__(self, other: object) -> bool:
        return not self == other
