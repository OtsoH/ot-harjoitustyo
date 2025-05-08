class Piece():
    """Yksittäistä pelilaudan ruutua kuvaava luokka."""

    def __init__(self, has_mine):
        """Alustaa Piece-olion.

        Args:
            has_mine: True tai False riippuen, onko ruudussa miina.
        """
        self.has_mine = has_mine
        self.revealed = False
        self.flagged = False
        self.num = 0
        self.neighbours = []

    def get_has_mine(self):
        """Palauttaa True, jos ruudussa on miina."""
        return self.has_mine

    def get_revealed(self):
        """Palauttaa True, jos ruutu on paljastettu."""
        return self.revealed

    def get_flagged(self):
        """Palauttaa True, jos ruutu on liputettu."""
        return self.flagged

    def set_neighbours(self, neighbours):
        """Asettaa ruudun naapurit ja laskee viereisten miinojen määrän.

        Args:
            neighbours: Lista Piece-olioista, jotka ovat naapureita.
        """
        self.neighbours = neighbours
        self.set_num()

    def get_neighbours(self):
        """Palauttaa ruudun naapurit."""
        return self.neighbours

    def set_num(self):
        """Laskee ja asettaa viereisten miinojen määrän."""
        self.num = 0
        for piece in self.neighbours:
            if piece.get_has_mine():
                self.num += 1

    def get_num(self):
        """Palauttaa viereisten miinojen määrän."""
        return self.num

    def set_flagged(self):
        """Asettaa tai poistaa lipun ruudusta."""
        self.flagged = not self.flagged

    def click(self):
        """Paljastaa ruudun."""
        self.revealed = True
