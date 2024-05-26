"""Game entrypoint"""

import numpy as np
import pygame
from pygame.surface import Surface
from pygame.locals import *
import tkinter.simpledialog
import tkinter.messagebox

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


def render_level(to_render: Level, display_surf: Surface, selection_pos: np.array = np.array([-1])):
    """Renders a level"""
    display_surf.fill((0, 0, 0))

    wall = pygame.image.load("assets/wall.png").convert()
    dest = pygame.image.load("assets/dest.png").convert()
    nothing = pygame.image.load("assets/nothing.png").convert()

    box = pygame.image.load("assets/box.png").convert_alpha()
    box_on_dest = pygame.image.load("assets/box_on_dest.png").convert_alpha()
    player = pygame.image.load("assets/player.png").convert_alpha()
    selection = pygame.image.load("assets/selection.png").convert_alpha()

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
        if to_render.matrix[boxPos] == constants.DESTINATION:
            display_surf.blit(box_on_dest, (boxPos[0] * img_size, boxPos[1] * img_size))
        else:
            display_surf.blit(box, (boxPos[0] * img_size, boxPos[1] * img_size))
    # draw player
    display_surf.blit(player,
                      (to_render.game_status.player_pos[0] * img_size, to_render.game_status.player_pos[1] * img_size))
    if selection_pos[0] != -1:
        display_surf.blit(selection, (selection_pos[0] * img_size, selection_pos[1] * img_size))
    pygame.display.update()
    return


def get_new_display_surf(shape: (int, int)):
    img_size = pygame.image.load("assets/nothing.png").get_width()
    return pygame.display.set_mode((img_size * shape[0], img_size * shape[1]))


def play_level(filepath: str):
    """Lets player play a level"""
    level = None
    try:
        level = Level(True, filepath)
    except ValueError as e:
        tkinter.messagebox.showerror("Error", "Failed to load level: " + str(e))
        return
    except Exception as e:
        tkinter.messagebox.showerror("Error", "An unexpected error occurred: " + str(e))
        return
    display_surf = get_new_display_surf(level.matrix.shape)
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
        if action == Action.RESET:
            try:
                level.handle_action(action)
            except ValueError as e:
                tkinter.messagebox.showerror("Error", "Failed to reload level: " + str(e))
                return
            except Exception as e:
                tkinter.messagebox.showerror("Error", "An unexpected error occurred: " + str(e))
                return
            running = not level.is_win()
            continue
        if action in [Action.MOVE_UP, Action.MOVE_RIGHT, Action.MOVE_DOWN, Action.MOVE_LEFT]:
            level.handle_action(action)
            running = not level.is_win()
            continue
        raise ValueError("Unknown value of action")
    pygame.display.quit()
    if level.is_win():
        tkinter.messagebox.showinfo("Congratulations",
                                    "You won!\nYour score: " + str(level.moves) + "\nOptimal moves: " + str(
                                        level.optimal_moves))


def ask_new_size() -> (int, int):
    new_width = 0
    while new_width <= 0 or new_width >= 20:
        new_width = tkinter.simpledialog.askinteger("Resizing dialog", "Please enter new width:")
        if new_width is None:
            return -1, -1

    new_height = 0
    while new_height <= 0 or new_height >= 20:
        new_height = tkinter.simpledialog.askinteger("Resizing dialog", "Please enter new height:")
        if new_height is None:
            return -1, -1
    return new_width, new_height


def resize_matrix(matrix: np.ndarray, new_size: (int, int)) -> np.ndarray:
    delta_width = new_size[0] - matrix.shape[0]
    delta_height = new_size[1] - matrix.shape[1]
    if delta_width > 0:
        matrix = np.pad(matrix, ((0, delta_width), (0, 0)), mode='constant', constant_values=0)
    elif delta_width < 0:
        matrix = matrix[:delta_width, :].copy()
    if delta_height > 0:
        matrix = np.pad(matrix, ((0, 0), (0, delta_height)), mode='constant', constant_values=0)
    elif delta_height < 0:
        matrix = matrix[:, :delta_height].copy()
    return matrix


def edit_level(level: Level):
    display_surf = get_new_display_surf(level.matrix.shape)
    pygame.display.set_caption("Sokoban - Editing a level")

    selection_pos = np.zeros(2, np.int8)
    running = True
    while running:
        render_level(level, display_surf, selection_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_LEFT:
                    if selection_pos[0] > 0:
                        selection_pos[0] -= 1
                    continue
                if event.key == pygame.K_RIGHT:
                    if selection_pos[0] < level.matrix.shape[0] - 1:
                        selection_pos[0] += 1
                    continue
                if event.key == pygame.K_UP:
                    if selection_pos[1] > 0:
                        selection_pos[1] -= 1
                    continue
                if event.key == pygame.K_DOWN:
                    if selection_pos[1] < level.matrix.shape[1] - 1:
                        selection_pos[1] += 1
                    continue
                if event.key == pygame.K_r:
                    new_size = ask_new_size()
                    if new_size[0] == -1:
                        continue
                    level.matrix = resize_matrix(level.matrix.copy(), new_size)
                    display_surf = get_new_display_surf(level.matrix.shape)
                    continue
                pos = tuple(selection_pos)
                if event.key == pygame.K_w:
                    if np.array_equal(selection_pos, level.game_status.player_pos):
                        continue
                    if pos in level.game_status.box_pos:
                        continue
                    level.matrix[pos] = constants.WALL
                    continue
                if event.key == pygame.K_d:
                    level.matrix[pos] = constants.DESTINATION
                    continue
                if event.key == pygame.K_n:
                    level.matrix[pos] = constants.NOTHING
                    continue
                if event.key == pygame.K_b:
                    if level.matrix[pos] == constants.WALL:
                        continue
                    if np.array_equal(selection_pos, level.game_status.player_pos):
                        continue
                    new_box_pos = set(level.game_status.box_pos)
                    if pos in level.game_status.box_pos:
                        new_box_pos.remove(pos)
                    else:
                        new_box_pos.add(pos)
                    level.game_status.box_pos = frozenset(new_box_pos)
                    continue
                if event.key == pygame.K_p:
                    if level.matrix[pos] == constants.WALL:
                        continue
                    if pos in level.game_status.box_pos:
                        continue
                    level.game_status.player_pos = selection_pos.copy()
                    continue

    # this can be done a lot better
    while level.filepath == "":
        new_path = tkinter.simpledialog.askstring("Sokoban dialogue", "Please enter a name for the level")
        if new_path is None:
            return
        level.filepath = "./levels/" + new_path + ".lvl"
    try:
        level.save()
    except Exception as e:
        tkinter.messagebox.showerror("Error", "An unexpected exception occurred: " + str(e))


def choice_menu(menu_name: str, choices: list) -> int:
    """Lets the player choose an option"""
    display_surf = pygame.display.set_mode((500, 500))
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
    if choice > 0:
        play_level("./levels/" + choices[choice] + ".lvl")


def choose_level_edit():
    choices = [f.stem for f in Path("./levels").iterdir() if f.is_file() and f.name.endswith(".lvl")]
    choices.insert(0, "Go back")
    choices.insert(1, "Create new")
    choice = choice_menu("Choose level", choices)
    if choice <= 0:
        return
    to_edit = Level(False)
    if choice != 1:
        try:
            to_edit = Level(False, "./levels/" + choices[choice] + ".lvl")
        except ValueError as e:
            tkinter.messagebox.showerror("Error", "Failed to load level: " + str(e))
            return
    edit_level(to_edit)


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
            choose_level_edit()
            continue
        running = False
    pygame.quit()


main()
