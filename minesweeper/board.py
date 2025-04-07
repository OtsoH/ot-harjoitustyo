from random import random
from piece import Piece

class Board():
    def __init__(self, size, prob):
        self.lost = False
        self.won = False
        self.size = size
        self.prob = prob
        self.num_clicked = 0
        self.num_non_mines = 0
        self.set_board()

    def set_board(self):
        self.board = []
        for _ in range(self.size[0]):
            row = []
            for _ in range(self.size[1]):
                has_mine = random() < self.prob
                if not has_mine:
                    self.num_non_mines += 1
                piece = Piece(has_mine)
                row.append(piece)
            self.board.append(row)
        self.set_neighbours()

    def get_size(self):
        return self.size

    def get_piece(self, idx):
        return self.board[idx[0]][idx[1]]

    def set_neighbours(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                neighbours = self.get_neighbours((row, col))
                piece.set_neighbours(neighbours)

    def get_neighbours(self, idx):
        neighbours = []
        for row in range(idx[0] - 1, idx[0] + 2):
            for col in range(idx[1] - 1, idx[1] + 2):
                out_of_bounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == idx[0] and col == idx[1]
                if out_of_bounds or same:
                    continue
                neighbours.append(self.get_piece((row, col)))
        return neighbours

    def clicking(self, piece, flag):
        if piece.get_revealed() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.set_flagged()
            return
        piece.click()
        if piece.get_has_mine():
            self.lost = True
            return
        self.num_clicked += 1
        if piece.get_num() != 0:
            return
        for neighbour in piece.get_neighbours():
            if not neighbour.get_has_mine() and not neighbour.get_revealed():
                self.clicking(neighbour, False)


    def get_lost(self):
        return self.lost

    def get_won(self):
        return self.num_non_mines == self.num_clicked
