"""Class that represents the current game status, such as the player position and positions of boxes"""

import numpy as np

from Action import Action

class GameStatus:
    """Class that represents the current game status, such as the player position and positions of boxes"""
    def __init__(self, playerPos: np.array, boxPos: set):
        self.playerPos = playerPos
        self.boxPos = boxPos.copy()

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

        newpos = (self.playerPos[0] + movevector[0], self.playerPos[1] + movevector[1])
        if matrix[newpos[0]][newpos[1]] == 1: # attempted to move into a wall
            return
        
        if newpos not in self.boxPos:
            self.playerPos = newpos
            return
        
        # there's a box
        # todo: check if I'm attempting a move into a wall with box or into a box with box
        # todo: handle calculation of new box set

