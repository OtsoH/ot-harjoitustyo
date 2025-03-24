from game import Game
from board import Board

size = (9,9)
board = Board(size)
screenSize = (800, 800)
game = Game(board, screenSize)
game.run()
