# pylint: disable=no-member
import pygame
from game import Game
from board import Board

def configure_screen(settings, max_cell_size=50):
    """Määrittää pelilaudan ja ikkunan koon vaikeustason mukaan.

    Args:
        settings (tuple): (rivit, sarakkeet, miinojen todennäköisyys)
        max_cell_size (int): Yksittäisen ruudun maksimikoko pikseleinä.

    Returns:
        tuple: (board_size, screen_size, prob)
    """
    size_x, size_y, prob = settings
    board_size = (size_x, size_y)
    screen_width = size_y * max_cell_size
    screen_height = size_x * max_cell_size
    screen_size = (screen_width, screen_height)

    return board_size, screen_size, prob

def run_game_loop(settings, max_cell_size=50):
    """Suorittaa yhden pelisilmukan valituilla asetuksilla.

    Args:
        settings (tuple): (rivit, sarakkeet, miinojen todennäköisyys)
        max_cell_size (int): Yksittäisen ruudun maksimikoko pikseleinä.

    Returns:
        False, jos peli lopetetaan, True jos käyttäjä haluaa pelata uudelleen.
    """
    if settings is None:
        return False

    board_size, _, prob = configure_screen(settings, max_cell_size)

    action = "retry"
    while action == "retry":
        board = Board(board_size, prob)
        game = Game(board, max_cell_size)
        action = game.run()

        if action is None:
            return False

    return True

def main():
    """Käynnistää pelin ja hallitsee päävalikkoa sekä pelisilmukkaa."""

    initial_size = 25
    menu_screen_size = (800, 800)
    try:
        continue_game = True
        while continue_game:
            dummy_board = Board((8, 8), 0.1)
            game = Game(dummy_board, initial_size, menu_screen_size)

            settings = game.main_menu()

            continue_game = run_game_loop(settings, initial_size)

    except pygame.error:
        pass

if __name__ == "__main__":
    main()
