from random import random
from piece import Piece

class Board():
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.setBoard()
    
    def setBoard(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                hasMine = random() < self.prob
                piece = Piece(hasMine)
                row.append(piece)
            self.board.append(row)
    
    def getSize(self):
        return self.size
    
    def getPiece(self, idx):
        return self.board[idx[0]][idx[1]]
        
    
   