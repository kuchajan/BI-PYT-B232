import pygame

from Action import Action


class Level:
    filepath = None
    matrix = []
    playerPosition = None
    boxPositions = None

    def reload(self):
        preload = []
        cols = -1
        with open(self.filepath, 'r') as f:
            for row in f.read().splitlines():
                preload.append(list(row))
                cols = cols if cols >= len(row) else len(row)
        rows = len(preload)

        for row in range(rows):
            row = []
            for col in range(cols):
                row.append(' ')
                # load from preload
                # check for special symbols:
                #
                # select appropriate symbol
            self.matrix.append(row)

    def load(self, filepath):
        self.filepath = filepath
        self.reload()

    def handle_action(self, action):
        if action == Action.EXIT:
            pygame.quit()
