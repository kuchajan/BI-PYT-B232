"""Class that represents an opened level the user is currently playing"""

import numpy as np

import constants as const
from game_status import GameStatus
from action import Action


class Level:
    """Class that represents an opened level the user is currently playing"""
    def get_dests(self):
        dests = set()
        for row in range(self.matrix.shape[1]):
            for col in range(self.matrix.shape[0]):
                if self.matrix[col][row] == const.DESTINATION:
                    dests.add((col, row))
        return frozenset(dests)

    def is_win(self, game_status: GameStatus = None):
        """Check that game_status is winning"""
        if game_status is None:
            game_status = self.game_status
        return game_status.box_pos == self.get_dests()

    def bfs(self):
        """Breadth first search that finds the optimal count of moves to solve level"""
        if len(self.game_status.box_pos) != len(self.get_dests()):
            return -1
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

    def load(self):
        """Loads a level from filepath"""
        if not isinstance(self.filepath, str) or len(self.filepath) == 0:
            raise ValueError("Cannot load level with given filepath")
        preload = []
        cols = -1
        with open(self.filepath, 'r', encoding="utf-8") as file:
            for row in file.read().splitlines():
                preload.append(row)
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)
        self.matrix = np.zeros((cols, rows), dtype=np.uint8)

        player_pos = np.array([-1, -1], np.int8)
        box_pos = set()

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
                # Box
                if curr_pos in "$B":
                    load_valid = True
                    box_pos.add((col, row))
                # Dest
                if curr_pos in ".PB":
                    load_valid = True
                    self.matrix[col][row] = const.DESTINATION
                if not load_valid:
                    raise ValueError("Invalid character loaded from file")
        self.game_status = GameStatus(player_pos, box_pos)

    def get_char(self, col: int, row: int) -> str:
        has_player = np.array_equal(self.game_status.player_pos, np.array([col, row], np.int8))
        has_box = ((col, row) in self.game_status.box_pos)
        if self.matrix[col][row] == const.WALL:
            if has_box or has_player:
                raise ValueError("Player nor box cannot be inside wall")
            return "#"
        if has_player and has_box:
            raise ValueError("Player cannot be inside box")
        if self.matrix[col][row] == const.NOTHING:
            if has_player:
                return "@"
            if has_box:
                return "$"
            return " "
        if self.matrix[col][row] == const.DESTINATION:
            if has_player:
                return "P"
            if has_box:
                return "B"
            return "."
        raise ValueError("Unknown value in level matrix")

    def save(self):
        with open(self.filepath, 'w', encoding="utf-8") as file:
            for row in range(self.matrix.shape[1]):
                str_to_write = ""
                for col in range(self.matrix.shape[0]):
                    str_to_write += self.get_char(col, row)
                file.write(str_to_write + "\n")

    def check_level(self):
        if self.game_status.player_pos[0] < 0 or self.game_status.player_pos[1] < 0:
            raise ValueError("No player was loaded")
        if len(self.game_status.box_pos) != len(self.get_dests()):
            raise ValueError("Level has incorrect count of objects")
        self.optimal_moves = self.bfs()
        if self.optimal_moves == -1:
            raise ValueError("Level is not solvable")
        

    def reload(self):
        """Reloads a level to play"""
        self.load()
        self.check_level()

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

    def __init__(self, play: bool, filepath: str = "", matrix=np.zeros((10, 10), dtype=np.uint8),
                 game_status=GameStatus(np.zeros(2, np.int8), set())):
        self.filepath = filepath
        if self.filepath == "":
            self.matrix = matrix
            self.game_status = game_status.copy()
        else:
            self.load()
        self.moves = 0
        self.optimal_moves = -1
        if play:
            self.check_level()
