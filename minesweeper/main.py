# pylint: disable=no-member
import pygame
from game import Game
from board import Board

def main():
    initial_size = (900, 900)
    try:
        while True:
            dummy_board = Board((8, 8), 0.1)
            game = Game(dummy_board, initial_size)

            settings = game.main_menu()
            if settings is None:
                return

            size_x, size_y, prob = settings
            board_size = (size_x, size_y)
            screen_size = (min(size_x * 32, 900), min(size_y * 32, 900))

            action = "retry"
            while action == "retry":
                board = Board(board_size, prob)
                game = Game(board, screen_size)
                action = game.run()

                if action is None:
                    return
    except pygame.error:
        pass

if __name__ == "__main__":
    main()
