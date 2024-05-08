"""Game entrypoint"""
# Game state: Main menu, Play menu, Playing level, Level editor menu, Editing level

# Main meWindow nu: Play, Level editor, Exit
# Play menu: Choose level, Back
# Level editor menu: Choose level, Create new, Back
import numpy as np
import pygame
from pygame.surface import Surface
from pygame.locals import *

import constants
# from game_status import GameStatus
from level import Level
from action import Action


def get_action():
    """Gets the action from the key being pressed"""
    pressed = pygame.key.get_pressed()
    if pressed[K_UP]:
        return Action.MOVE_UP
    if pressed[K_RIGHT]:
        return Action.MOVE_RIGHT
    if pressed[K_DOWN]:
        return Action.MOVE_DOWN
    if pressed[K_LEFT]:
        return Action.MOVE_LEFT
    if pressed[K_r]:
        return Action.RESET
    if pressed[K_ESCAPE]:
        return Action.EXIT
    return Action.NOTHING


def render_level(to_render: Level, surface: Surface):
    """Renders a level"""
    surface.fill((0, 0, 0))

    wall = pygame.image.load("assets/wall.png").convert()
    dest = pygame.image.load("assets/dest.png").convert()
    nothing = pygame.image.load("assets/nothing.png").convert()

    box = pygame.image.load("assets/box.png").convert_alpha()
    box_on_dest = pygame.image.load("assets/box_on_dest.png").convert_alpha()
    player = pygame.image.load("assets/player.png").convert_alpha()

    img_size = wall.get_width()  # images should be square

    # draw environment
    for i in range(0, to_render.matrix.shape[0]):
        for j in range(0, to_render.matrix.shape[1]):
            if to_render.matrix[i][j] == constants.WALL:
                surface.blit(wall, (i * img_size, j * img_size))
            elif to_render.matrix[i][j] == constants.DESTINATION:
                surface.blit(dest, (i * img_size, j * img_size))
            elif to_render.matrix[i][j] == constants.NOTHING:
                surface.blit(nothing, (i * img_size, j * img_size))
            else:
                raise ValueError("Unknown value read from level matrix")
    # draw boxes
    for boxPos in to_render.game_status.box_pos:
        if boxPos in to_render.dests:
            surface.blit(box_on_dest, (boxPos[0] * img_size, boxPos[1] * img_size))
        else:
            surface.blit(box, (boxPos[0] * img_size, boxPos[1] * img_size))
    # draw player
    surface.blit(player,
                 (to_render.game_status.player_pos[0] * img_size, to_render.game_status.player_pos[1] * img_size))
    print(to_render.game_status.player_pos)
    pygame.display.update()
    return


def play_level(filepath: str, display_surf: Surface):
    level = Level(filepath)
    running = True
    while running:
        render_level(level, display_surf)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                continue
        action = get_action()
        if action == Action.NOTHING:
            continue
        if action == Action.EXIT:
            running = False
            continue
        if action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.RESET]:
            level.handle_action(action)
            continue
        raise ValueError("Unknown value of action")


def main():
    """Entry function"""
    pygame.init()
    screen_width = 500
    screen_height = 500
    display_surf = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sokoban")

    play_level("levels/level1.lvl", display_surf)

    pygame.quit()


main()
