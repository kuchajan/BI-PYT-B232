"""Class that represents the current game status, such as the player position and positions of boxes"""

import numpy as np

import Constants as C
from Action import Action

class GameStatus:
    """Class that represents the current game status, such as the player position and positions of boxes"""
    def __init__(self, playerPos: np.array, boxPos: set):
        self.playerPos = playerPos
        self.boxPos = frozenset(boxPos)

    def copy(self):
        """Creates a copy of the instance"""
        return GameStatus(self.playerPos, self.boxPos)

    def handle_action(self, action: Action, matrix: np.array):
        """Handles a move action"""
        movevector = np.zeros((2), np.int8)
        if action == Action.MOVE_UP:
            # y--
            movevector[1] -= 1
        elif action == Action.MOVE_RIGHT:
            # x++
            movevector[0] += 1
        elif action == Action.MOVE_DOWN:
            # y++
            movevector[1] += 1
        elif action == Action.MOVE_LEFT:
            # x--
            movevector[0] -= 1
        else:
            # invalid action
            return self.copy()

        newpos = self.playerPos + movevector
        if matrix[newpos[0]][newpos[1]] == C.WALL: # attempted to move into a wall
            return self.copy()

        if tuple(newpos) not in self.boxPos:
            return GameStatus(newpos, self.boxPos)

        # there's a box
        newSingleBoxPos = newpos + movevector
        if matrix[newSingleBoxPos[0]][newSingleBoxPos[1]] == C.WALL or tuple(newSingleBoxPos) in self.boxPos:
            # moving box into wall or into box
            return self.copy()

        newBoxPos = set(self.boxPos)
        newBoxPos.remove(tuple(newpos))
        newBoxPos.add(tuple(newSingleBoxPos))
        return GameStatus(newpos, newBoxPos)
    
    def __hash__(self) -> int:
        return hash((tuple(self.playerPos), self.boxPos))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, GameStatus) and np.array_equal(self.playerPos, other.playerPos) and self.boxPos == other.boxPos

    def __ne__(self, other: object) -> bool:
        return not self == other
