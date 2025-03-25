from game import Game
from board import Board

prob = 0.2
size = (32,32)
board = Board(size, prob)
screenSize = (900, 900)
game = Game(board, screenSize)
game.run()
