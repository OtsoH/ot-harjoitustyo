# pylint: disable=no-member
import pygame
from game import Game
from board import Board

def _configure_screen(settings):
    """Määrittää pelilaudan ja ikkunan koon vaikeustason mukaan.

    Args:
        settings (tuple): (rivit, sarakkeet, miinojen todennäköisyys)

    Returns:
        tuple: (board_size, screen_size, prob)
    """
    size_x, size_y, prob = settings
    board_size = (size_x, size_y)

    if size_x == 8 and size_y == 8:
        screen_width = size_x * 50
        screen_height = size_y * 50
    elif size_x == 16 and size_y == 16:
        screen_width = size_x * 30
        screen_height = size_y * 30
    else:
        screen_width =  size_x * 25
        screen_height = size_y * 25

    screen_size = (screen_width, screen_height)
    return board_size, screen_size, prob

def _run_game_loop(settings):
    """Suorittaa yhden pelisilmukan valituilla asetuksilla.

    Args:
        settings (tuple): (rivit, sarakkeet, miinojen todennäköisyys)

    Returns:
        False, jos peli lopetetaan, True jos käyttäjä haluaa pelata uudelleen.
    """
    if settings is None:
        return False

    board_size, screen_size, prob = _configure_screen(settings)

    action = "retry"
    while action == "retry":
        board = Board(board_size, prob)
        game = Game(board, screen_size)
        action = game.run()

        if action is None:
            return False

    return True

def main():
    """Käynnistää pelin ja hallitsee päävalikkoa sekä pelisilmukkaa."""

    initial_size = (900, 900)
    try:
        continue_game = True
        while continue_game:
            dummy_board = Board((8, 8), 0.1)
            game = Game(dummy_board, initial_size)

            settings = game.main_menu()

            continue_game = _run_game_loop(settings)

    except pygame.error:
        pass

if __name__ == "__main__":
    main()
