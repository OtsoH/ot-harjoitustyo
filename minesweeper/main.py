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

            if size_x == 8 and size_y == 8:
                screen_width = size_x * 50
                screen_height = size_y * 50
            elif size_x == 16 and size_y == 16:
                screen_width = size_x * 30
                screen_height = size_y * 30
            else:
                screen_width = size_x * 25
                screen_height = size_y * 25

            screen_size = (screen_width, screen_height)

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
