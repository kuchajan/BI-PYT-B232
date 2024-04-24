"""Class that represents an opened level the user is currently playing"""

import numpy as np

import Constants as C
from GameStatus import GameStatus
from Action import Action


class Level:
    """Class that represents an opened level the user is currently playing"""

    def is_win(self, gamestatus: GameStatus = None):
        """Check that gamestatus is winning"""
        return self.gamestatus.boxPos == self.dests if gamestatus is None else gamestatus.boxPos == self.dests

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
                toVisit = visiting.handle_action(action, self.matrix)
                if toVisit not in visited:
                    queue.append(toVisit)
                    visited[toVisit] = visited[visiting] + 1
        return -1

    def reload(self):
        """Reloads a level from filepath"""
        preload = []
        cols = -1
        # TODO: Handle edge cases like non-existing file, file deleted mid read, forbidden access etc.
        with open(self.filepath, 'r', encoding="utf-8") as f:
            for row in f.read().splitlines():
                preload.append(row)
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)
        self.matrix = np.zeros((rows,cols),dtype=np.uint8)

        playerCount = 0

        playerPos = np.zeros((2), np.int8)
        boxPos = set()
        destsTmp = set()

        for row in range(rows):
            for col in range(cols):
                currPos = ' ' if len(preload[row]) <= col else preload[row][col]
                # nothing
                if currPos == ' ':
                    self.matrix[row][col] = const.NOTHING
                    continue
                # wall
                if currPos == '#':
                    self.matrix[row][col] = const.WALL
                    continue
                loadedSomething = False
                # Player
                if currPos in "@P":
                    loadedSomething = True
                    playerPos = np.array([row, col], np.int8)
                    playerCount += 1
                # Box
                if currPos in "$B":
                    loadedSomething = True
                    boxPos.add((row, col))
                # Dest
                if currPos in ".PB":
                    loadedSomething = True
                    self.matrix[row][col] = const.DESTINATION
                    destsTmp.add((row, col))
                if not loadedSomething:
                    raise ValueError("Invalid character loaded from file")

        if (playerCount != 1 or len(boxPos) != len(destsTmp)):
            raise ValueError("Level has incorrect count of objects")
        self.gamestatus = GameStatus(playerPos, boxPos)
        self.dests = frozenset(destsTmp)

        self.optimalMoves = self.bfs()
        if (self.optimalMoves == -1):
            raise ValueError("Level is not solveable")

    def __init__(self, filePath):
        self.filepath = filePath
        self.matrix = np.zeros((0,0), dtype=np.uint8)
        self.dests = frozenset()
        self.gamestatus = GameStatus(np.zeros((2), np.int8), set())
        self.moves = 0
        self.optimalMoves = -1
        self.reload()
