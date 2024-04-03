"""Class that represents an opened level the user is currently playing"""

import numpy as np
import pygame as pg

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
                preload.append(list(row))
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)
        self.matrix = np.zeros((rows,cols),dtype=np.uint8)

        for row in range(rows):
            for col in range(cols):
                currPos = ' ' if len(preload[row]) <= col else preload[row][col]
                # All possible things
                # #: wall
                # @: player
                # $: box
                # .: dest
                # P: Player on dest
                # B: Box on dest
                


    def __init__(self, filePath):
        self.filepath = filePath
        self.matrix = np.zeros((0,0), dtype=np.uint8)
        self.playerPosition = None
        self.boxPositions = []
        self.reload()
