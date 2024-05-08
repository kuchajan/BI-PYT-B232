"""Game entrypoint"""

import pygame
from pygame.surface import Surface
from pygame.locals import *

from pathlib import Path

import constants
from level import Level
from action import Action


def get_action() -> Action:
    """Gets the action from pygame events"""
    for event in pygame.event.get():
        if event.type == QUIT:
            return Action.EXIT
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return Action.EXIT
            if event.key == K_RETURN or event.key == K_KP_ENTER:
                return Action.ENTER
            if event.key == K_r:
                return Action.RESET
            if event.key == K_UP:
                return Action.MOVE_UP
            if event.key == K_RIGHT:
                return Action.MOVE_RIGHT
            if event.key == K_DOWN:
                return Action.MOVE_DOWN
            if event.key == K_LEFT:
                return Action.MOVE_LEFT
    return Action.NOTHING


def get_text_surface(string: str, size: int):
    """Sort of a macro to render a text to surface"""
    return pygame.font.SysFont(pygame.font.get_default_font(), size).render(string, True, (255, 255, 255))


def render_choice_menu(menu_name: str, choices: list, current_choice: int, display_surf: Surface):
    display_surf.fill((0, 0, 0))
    name_surf = get_text_surface(menu_name, 50)
    name_surf_pos = ((display_surf.get_width() - name_surf.get_width()) // 2, 10)
    display_surf.blit(name_surf, name_surf_pos)

    for i in range(-5, 6):  # from -5 to 5
        rendering_choice = current_choice + i
        if rendering_choice < 0 or rendering_choice >= len(choices):
            continue
        choice_surf = get_text_surface(("> " if i == 0 else "") + choices[rendering_choice], 30)
        choice_surf_pos = ((display_surf.get_width() - choice_surf.get_width()) // 2,
                           200 + i * (choice_surf.get_height() + 3))
        display_surf.blit(choice_surf, choice_surf_pos)
    pygame.display.update()


def render_level(to_render: Level, display_surf: Surface):
    """Renders a level"""
    display_surf.fill((0, 0, 0))

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
                display_surf.blit(wall, (i * img_size, j * img_size))
            elif to_render.matrix[i][j] == constants.DESTINATION:
                display_surf.blit(dest, (i * img_size, j * img_size))
            elif to_render.matrix[i][j] == constants.NOTHING:
                display_surf.blit(nothing, (i * img_size, j * img_size))
            else:
                raise ValueError("Unknown value read from level matrix")
    # draw boxes
    for boxPos in to_render.game_status.box_pos:
        if boxPos in to_render.dests:
            display_surf.blit(box_on_dest, (boxPos[0] * img_size, boxPos[1] * img_size))
        else:
            display_surf.blit(box, (boxPos[0] * img_size, boxPos[1] * img_size))
    # draw player
    display_surf.blit(player,
                      (to_render.game_status.player_pos[0] * img_size, to_render.game_status.player_pos[1] * img_size))
    pygame.display.update()
    return


def play_level(filepath: str):
    """Lets player play a level"""
    level = Level(filepath)
    img_size = pygame.image.load("assets/nothing.png").get_width()
    screen_width = img_size * level.matrix.shape[0]
    screen_height = img_size * level.matrix.shape[1]
    display_surf = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sokoban - " + filepath)

    running = True
    while running:
        render_level(level, display_surf)
        action = get_action()
        if action in [Action.NOTHING, Action.ENTER]:
            continue
        if action == Action.EXIT:
            running = False
            continue
        if action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT, Action.RESET]:
            level.handle_action(action)
            if level.is_win():
                running = False
            continue
        raise ValueError("Unknown value of action")


def choice_menu(menu_name: str, choices: list) -> int:
    """Lets the player choose an option"""
    screen_width = 500
    screen_height = 500
    display_surf = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sokoban")

    current_choice = 0
    running = True
    while running:
        render_choice_menu(menu_name, choices, current_choice, display_surf)
        action = get_action()
        if action in [Action.NOTHING, Action.MOVE_LEFT, Action.MOVE_RIGHT]:
            continue
        if action == Action.EXIT:
            running = False
            current_choice = -1
            continue
        if action == Action.ENTER:
            running = False
            continue
        if action == Action.RESET:
            current_choice = 0
            continue
        if action == Action.MOVE_UP:
            if current_choice > 0:
                current_choice -= 1
            continue
        if action == Action.MOVE_DOWN:
            if current_choice < len(choices) - 1:
                current_choice += 1
            continue
        raise ValueError("Unknown value of action")

    return current_choice


def choose_level_play():
    choices = [f.stem for f in Path("./levels").iterdir() if f.is_file() and f.name.endswith(".lvl")]
    choices.insert(0, "Go back")
    choice = choice_menu("Choose level", choices)
    if choice <= 0:
        return
    play_level("./levels/" + choices[choice] + ".lvl")


def main():
    """Entry function"""
    pygame.init()
    pygame.font.init()
    running = True
    while running:
        choices = ["Play", "Edit", "Exit"]
        choice = choice_menu("Sokoban", choices)
        if choice == 0:
            choose_level_play()
            continue
        if choice == 1:
            # choose_level_edit()
            continue
        running = False
    pygame.quit()


main()
