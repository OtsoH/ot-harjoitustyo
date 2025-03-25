from game import Game
from board import Board

size = (32,32)
board = Board(size)
screenSize = (900, 900)
game = Game(board, screenSize)
game.run()
