import random
from piece import Piece

class Board():
    """Pelilaudan logiikasta vastaava luokka."""
    def __init__(self, size, num_mines):
        """Alustaa pelilaudan

        Args:
            size: Koko, johon pelilauta alustetaan (rivit, sarakkeet)
            num_mines: Miinojen määrä.
        """
        self.lost = False
        self.won = False
        self.size = size
        self.num_clicked = 0
        self.num_non_mines = 0
        self.clicked_mine = None
        self.set_board(num_mines)

    def set_board(self, num_mines):
        """Luo uuden pelilaudan ja asettaa miinat satunnaisesti.

        Args:
            num_mines: Miinojen määrä.
        """

        num_mines = int(num_mines)

        self.board = [[Piece(False) for _ in range(self.size[1])] for _ in range(self.size[0])]

        all_positions = [(row, col) for row in range(self.size[0]) for col in range(self.size[1])]
        mine_positions = random.sample(all_positions, num_mines)

        for row, col in mine_positions:
            self.board[row][col] = Piece(True)

        self.set_neighbours()
        self.num_non_mines = self.size[0] * self.size[1] - num_mines

    def get_size(self):
        """Palauttaa laudan koon.

        Returns:
            tuple: (rivit, sarakkeet)
        """
        return self.size

    def get_piece(self, idx):
        """Palauttaa annetussa indeksissä olevan Piece-olion.

        Args:
            idx: (rivi, sarake)

        Returns:
            Piece: Haluttu ruutu
        """
        return self.board[idx[0]][idx[1]]

    def set_neighbours(self):
        """Asettaa jokaiselle ruudulle sen naapurit."""
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece((row, col))
                neighbours = self.get_neighbours((row, col))
                piece.set_neighbours(neighbours)

    def get_neighbours(self, idx):
        """Palauttaa annetun ruudun naapurit.

        Args:
            idx: (rivi, sarake)

        Returns:
            Palauttaa listan Piece-olioista, jotka ovat naapureita
        """
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
        """Käsittelee ruudun paljastuksen ja liputuksen.

        Args:
            piece: Klikattu ruutu.
            flag: True, jos asetetaan lippu.
        """
        if piece.get_revealed() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.set_flagged()
            return
        piece.click()
        if piece.get_has_mine():
            self.lost = True
            self.clicked_mine = piece
            return
        self.num_clicked += 1

        if piece.get_num() != 0:
            return
        for neighbour in piece.get_neighbours():
            if not neighbour.get_has_mine() and not neighbour.get_revealed():
                self.clicking(neighbour, False)

    def get_lost(self):
        """Palauttaa True jos peli on hävitty."""
        return self.lost

    def get_won(self):
        """Palauttaa True jos peli on voitettu."""
        return self.num_non_mines == self.num_clicked

    def reveal_all(self):
        """Paljastaa kaikki avaamattomat ruudut."""
        for row in self.board:
            for piece in row:
                if piece.get_num() > 0:
                    piece.num = 0
                if not piece.get_revealed():
                    piece.click()
