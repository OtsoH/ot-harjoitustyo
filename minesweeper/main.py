# pylint: disable=no-member
import pygame
from game import Game
from board import Board
from database import GameDatabase

def configure_screen(settings, max_piece_size=50):
    """Määrittää pelilaudan ja ikkunan koon vaikeustason mukaan.

    Args:
        settings (tuple): (rivit, sarakkeet, miinojen määrä)
        max_piece_size (int): Yksittäisen ruudun maksimikoko pikseleinä.

    Returns:
        tuple: (board_size, screen_size)
    """
    size_x, size_y, prob = settings
    board_size = (size_x, size_y)
    screen_width = size_y * max_piece_size
    screen_height = size_x * max_piece_size
    screen_size = (screen_width, screen_height)

    return board_size, screen_size, prob

def run_game_loop(settings, max_piece_size=50, db=None):
    """Suorittaa yhden pelisilmukan valituilla asetuksilla."""
    board_size, _, num_mines = configure_screen(settings, max_piece_size)
    board = Board(board_size, num_mines)
    game = Game(board, max_piece_size, db=db)

    while True:
        result = game.run()

        if result == "retry":
            board = Board(board_size, num_mines)
            game = Game(board, max_piece_size, db=db)

        elif result == "main_menu":
            return True
        else:
            return False

def main():
    """Käynnistää pelin ja hallitsee päävalikkoa sekä pelisilmukkaa."""
    db = GameDatabase()

    initial_size = 25
    menu_screen_size = (800, 800)
    try:
        continue_game = True
        while continue_game:
            dummy_board = Board((8, 8), 1)
            game = Game(dummy_board, initial_size, menu_screen_size, db=db)

            settings = game.main_menu()
            if not settings:
                break

            continue_game = run_game_loop(settings, initial_size, db)

    except pygame.error:
        pass
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    main()
