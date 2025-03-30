class Piece():
    def __init__(self, hasMine):
        self.hasMine = hasMine
        self.revealed = False
        self.flagged = False
        

    def gethasMine(self):
        return self.hasMine
    
    def getrevealed(self):
        return self.revealed
    
    def getflagged(self):
        return self.flagged
    
    def setNeighbours(self, neighbours):
        self.neighbours = neighbours
        self.setNum()
    
    def setNum(self):
        self.num = 0
        for piece in self.neighbours:
            if (piece.gethasMine()):
                self.num += 1
        
    def getNum(self):
        return self.num