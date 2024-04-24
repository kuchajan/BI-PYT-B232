"""Class that represents an opened level the user is currently playing"""

import numpy as np
import pygame as pg

import Constants as C
from GameStatus import GameStatus
from Action import Action


class Level:
    """Class that represents an opened level the user is currently playing"""

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
        boxCount = 0
        destCount = 0

        playerPos = np.zeros((2), np.int8)
        boxPos = set()

        for row in range(rows):
            for col in range(cols):
                currPos = ' ' if len(preload[row]) <= col else preload[row][col]
                if currPos == ' ':
                    self.matrix[row][col] = C.NOTHING
                elif currPos == '#':
                    self.matrix[row][col] = C.WALL
                elif currPos == '.':
                    self.matrix[row][col] = C.DESTINATION
                    destCount += 1
                elif currPos == '@':
                    playerPos = np.array([row, col], np.int8)
                    playerCount += 1
                elif currPos == 'P':
                    self.matrix[row][col] = C.DESTINATION
                    destCount += 1
                    playerPos = np.array([row, col], np.int8)
                    playerCount += 1
                elif currPos == '$':
                    boxPos.add(np.array([row, col], np.int8))
                    boxCount += 1
                elif currPos == 'B':
                    boxPos.add(np.array([row, col], np.int8))
                    boxCount += 1
                    self.matrix[row][col] = C.DESTINATION
                    destCount += 1
                else:
                    raise ValueError("Invalid character loaded from file")

        if (playerCount != 1 or boxCount != destCount):
            raise ValueError("Level has incorrect count of objects")
        self.gamestatus = GameStatus(playerPos, boxPos)

    def __init__(self, filePath):
        self.filepath = filePath
        self.matrix = np.zeros((0,0), dtype=np.uint8)
        self.gamestatus = GameStatus(np.zeros((2), np.int8), set())
        self.reload()
