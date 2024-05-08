"""Class that represents an opened level the user is currently playing"""

import numpy as np

import constants as const
from game_status import GameStatus
from action import Action


class Level:
    """Class that represents an opened level the user is currently playing"""

    def is_win(self, game_status: GameStatus = None):
        """Check that game_status is winning"""
        return self.game_status.box_pos == self.dests if game_status is None else game_status.box_pos == self.dests

    def bfs(self):
        """Breadth first search that finds the optimal count of moves to solve level"""
        visited = {self.game_status: 0}
        queue = [self.game_status]
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
        if not isinstance(self.filepath, str) or len(self.filepath) == 0:
            raise ValueError("Cannot load level with given filepath")
        preload = []
        cols = -1
        # TODO: Handle edge cases like non-existing file, file deleted mid read, forbidden access etc.
        with open(self.filepath, 'r', encoding="utf-8") as file:
            for row in file.read().splitlines():
                preload.append(row)
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)
        self.matrix = np.zeros((cols, rows), dtype=np.uint8)

        player_cnt = 0

        player_pos = np.zeros(2, np.int8)
        box_pos = set()
        dests_tmp = set()

        for row in range(rows):
            for col in range(cols):
                curr_pos = ' ' if len(preload[row]) <= col else preload[row][col]
                # nothing
                if curr_pos == ' ':
                    self.matrix[col][row] = const.NOTHING
                    continue
                # wall
                if curr_pos == '#':
                    self.matrix[col][row] = const.WALL
                    continue
                load_valid = False
                # Player
                if curr_pos in "@P":
                    load_valid = True
                    player_pos = np.array([col, row], np.int8)
                    player_cnt += 1
                # Box
                if curr_pos in "$B":
                    load_valid = True
                    box_pos.add((col, row))
                # Dest
                if curr_pos in ".PB":
                    load_valid = True
                    self.matrix[col][row] = const.DESTINATION
                    dests_tmp.add((col, row))
                if not load_valid:
                    raise ValueError("Invalid character loaded from file")

        if player_cnt != 1 or len(box_pos) != len(dests_tmp):
            raise ValueError("Level has incorrect count of objects")
        self.game_status = GameStatus(player_pos, box_pos)
        self.dests = frozenset(dests_tmp)

        self.optimal_moves = self.bfs()
        if self.optimal_moves == -1:
            raise ValueError("Level is not solveable")

    def handle_action(self, action: Action):
        """Handles an action from the user"""
        if action == Action.RESET:
            self.moves = 0
            self.reload()
            return
        if action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT]:
            new_game_status = self.game_status.handle_action(action, self.matrix)
            if new_game_status != self.game_status:
                self.moves += 1
                self.game_status = new_game_status
            return
        if action == Action.NOTHING:
            return
        raise ValueError("Invalid action passed to level")

    def __init__(self, filepath: str = "", matrix=np.zeros((0, 0), dtype=np.uint8), dests=frozenset(),
                 game_status=GameStatus(np.zeros(2, np.int8), set())):
        self.filepath = filepath
        self.matrix = matrix
        self.dests = dests.copy()
        self.game_status = game_status.copy()
        self.optimal_moves = -1
        self.moves = 0
        if filepath != "":
            self.reload()
        else:
            self.optimal_moves = self.bfs()
            if self.optimal_moves == -1:
                raise ValueError("Level is not solvable")
