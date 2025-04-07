class Piece():
    def __init__(self, has_mine):
        self.has_mine = has_mine
        self.revealed = False
        self.flagged = False
        self.num = 0
        self.neighbours = []

    def get_has_mine(self):
        return self.has_mine

    def get_revealed(self):
        return self.revealed

    def get_flagged(self):
        return self.flagged

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours
        self.set_num()

    def get_neighbours(self):
        return self.neighbours

    def set_num(self):
        self.num = 0
        for piece in self.neighbours:
            if piece.get_has_mine():
                self.num += 1

    def get_num(self):
        return self.num

    def set_flagged(self):
        self.flagged = not self.flagged

    def click(self):
        self.revealed = True
