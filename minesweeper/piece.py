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