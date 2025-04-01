from random import random
from piece import Piece

class Board():
    def __init__(self, size, prob):
        self.lost = False
        self.won = False
        self.size = size
        self.prob = prob
        self.numClicked = 0
        self.numNonMines = 0
        self.setBoard()
    
    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasMine = random() < self.prob
                if (not hasMine):
                    self.numNonMines += 1
                piece = Piece(hasMine)
                row.append(piece)
            self.board.append(row)
        self.setNeighbours()
    
    def getSize(self):
        return self.size
    
    def getPiece(self, idx):
        return self.board[idx[0]][idx[1]]
    
    def setNeighbours(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.getPiece((row, col))
                neighbours = self.getNeighbours((row, col))
                piece.setNeighbours(neighbours)
    
    def getNeighbours(self, idx):
        neighbours = []
        for row in range(idx[0] - 1, idx[0] + 2):
            for col in range(idx[1] - 1, idx[1] + 2):
                outOfBounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == idx[0] and col == idx[1]
                if (outOfBounds or same):
                    continue
                neighbours.append(self.getPiece((row, col)))
        return neighbours
    
    def clicking(self, piece, flag):
        if (piece.getrevealed() or (not flag and piece.getflagged())):
            return
        if (flag):
            piece.setflagged()
            return
        piece.click()
        if (piece.gethasMine()):
            self.lost = True
            return
        self.numClicked += 1
        if (piece.getNum() != 0):
            return
        for neighbour in piece.getNeighbours():
            if (not neighbour.gethasMine() and not neighbour.getrevealed()):
                self.clicking(neighbour, False)
        
        
    def getlost(self):
        return self.lost

    def getwon(self):
        return self.numNonMines == self.numClicked
    