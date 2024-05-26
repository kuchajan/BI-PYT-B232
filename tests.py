"""Tests for GameStatus"""
import pytest

import numpy as np

import constants as const
from action import Action
from game_status import GameStatus
from level import Level


def test_game_status_copy():
    """Tests that copy creates a copy that doesn't affect parent nor children"""
    subject1 = GameStatus(np.array([1, 1]), {(2, 2)})
    subject2 = subject1.copy()
    assert subject1 == subject2

    subject1.player_pos = np.array([1, 2])
    assert subject1 != subject2

    subject2.player_pos = np.array([3, 3])
    assert subject1 != subject2

    subject1.player_pos = np.array([1, 1])
    subject2.player_pos = np.array([1, 1])
    subject1.box_pos = frozenset((3, 3))
    assert subject1 != subject2

    subject2.box_pos = frozenset((4, 4))
    assert subject1 != subject2


def test_game_status_handle_action():
    """Tests that game status handles action correctly"""
    level_matrix = np.zeros((5, 5), np.uint8)
    level_matrix[2][4] = const.WALL
    subject = GameStatus(np.array([2, 0]), {(2, 2)})
    # succesful free move
    subject = subject.handle_action(Action.MOVE_DOWN, level_matrix)
    assert np.array_equal(subject.player_pos, np.array([2, 1]))
    assert subject.box_pos == {(2, 2)}
    # successful push box
    subject = subject.handle_action(Action.MOVE_DOWN, level_matrix)
    assert np.array_equal(subject.player_pos, np.array([2, 2]))
    assert subject.box_pos == {(2, 3)}
    # unsuccessful push box into wall
    subject = subject.handle_action(Action.MOVE_DOWN, level_matrix)
    assert np.array_equal(subject.player_pos, np.array([2, 2]))
    assert subject.box_pos == {(2, 3)}

    subject = GameStatus(np.array([2, 3]), {(2, 1), (2, 2)})
    # unsuccessful move into wall
    subject = subject.handle_action(Action.MOVE_DOWN, level_matrix)
    assert np.array_equal(subject.player_pos, np.array([2, 3]))
    assert subject.box_pos == {(2, 1), (2, 2)}
    # unsuccessful push box into box
    subject = subject.handle_action(Action.MOVE_UP, level_matrix)
    assert np.array_equal(subject.player_pos, np.array([2, 3]))
    assert subject.box_pos == {(2, 1), (2, 2)}


def test_level_load_positive():
    """A positive test that checks whether the level is loaded correctly"""
    level = Level(False, "./levels/tutorial.lvl")
    assert np.array_equal(level.matrix, np.array([[1, 1, 1, 1, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 0, 2, 0, 1],
                                                  [1, 0, 0, 0, 1],
                                                  [1, 1, 1, 1, 1]], np.uint8))
    assert np.array_equal(level.game_status.player_pos, np.array([2, 2], np.int8))
    assert level.game_status.box_pos == {(4, 2)}


def test_level_load_negative():
    """Negative tests for Level load method"""
    with pytest.raises(ValueError):
        Level(False, "./levels/test_levels/invalid_char.lvl")
    with pytest.raises(FileNotFoundError):
        Level(False, "./levels/nonexistent.lvl")


def test_level_bfs():
    """Tests that check whether bfs works correctly"""
    assert Level(False, "./levels/tutorial.lvl").bfs() == 3
    assert Level(False, "./levels/test_levels/too_many_boxes.lvl").bfs() == -1
    assert Level(False, "./levels/test_levels/unsolvable.lvl").bfs() == -1
