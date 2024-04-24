"""Class that represents an opened level the user is currently playing"""

import numpy as np

import constants as Const
from game_status import GameStatus
from action import Action


class Level:
    """Class that represents an opened level the user is currently playing"""

    def is_win(self, gamestatus: GameStatus = None):
        """Check that gamestatus is winning"""
        return self.gamestatus.box_pos == self.dests if gamestatus is None else gamestatus.box_pos == self.dests

    def bfs(self):
        """Breadth first search that finds the optimal count of moves to solve level"""
        visited = {}
        visited[self.gamestatus] = 0
        queue = [self.gamestatus]
        while queue:
            visiting = queue.pop(0)
            if self.is_win(visiting):
                return visited[visiting]
            for action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT]:
                to_visit = visiting.handle_action(action, self.matrix)
                if to_visit not in visited:
                    queue.append(to_visit)
                    visited[to_visit] = visited[visiting] + 1
        return -1

    def reload(self):
        """Reloads a level from filepath"""
        preload = []
        cols = -1
        # TODO: Handle edge cases like non-existing file, file deleted mid read, forbidden access etc.
        with open(self.filepath, 'r', encoding="utf-8") as file:
            for row in file.read().splitlines():
                preload.append(row)
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)
        self.matrix = np.zeros((rows,cols),dtype=np.uint8)

        player_cnt = 0

        player_pos = np.zeros((2), np.int8)
        box_pos = set()
        dests_tmp = set()

        for row in range(rows):
            for col in range(cols):
                curr_pos = ' ' if len(preload[row]) <= col else preload[row][col]
                # nothing
                if curr_pos == ' ':
                    self.matrix[row][col] = Const.NOTHING
                    continue
                # wall
                if curr_pos == '#':
                    self.matrix[row][col] = Const.WALL
                    continue
                load_valid = False
                # Player
                if curr_pos in "@P":
                    load_valid = True
                    player_pos = np.array([row, col], np.int8)
                    player_cnt += 1
                # Box
                if curr_pos in "$B":
                    load_valid = True
                    box_pos.add((row, col))
                # Dest
                if curr_pos in ".PB":
                    load_valid = True
                    self.matrix[row][col] = Const.DESTINATION
                    dests_tmp.add((row, col))
                if not load_valid:
                    raise ValueError("Invalid character loaded from file")

        if (player_cnt != 1 or len(box_pos) != len(dests_tmp)):
            raise ValueError("Level has incorrect count of objects")
        self.gamestatus = GameStatus(player_pos, box_pos)
        self.dests = frozenset(dests_tmp)

        self.optimal_moves = self.bfs()
        if self.optimal_moves == -1:
            raise ValueError("Level is not solveable")

    def handle_action(self, action: Action):
        """Handles an action from the user"""
        if action == action.RESET:
            self.reload()
            return
        if action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT]:
            self.game_status = self.game_status.handle_action(action)
            return
        raise ValueError("Invalid action passed to level")

    def __init__(self, filepath):
        self.filepath = filepath
        self.matrix = np.zeros((0,0), dtype=np.uint8)
        self.dests = frozenset()
        self.game_status = GameStatus(np.zeros((2), np.int8), set())
        self.optimal_moves = -1
        self.reload()
