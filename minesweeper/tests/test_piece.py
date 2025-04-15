import unittest
from piece import Piece

class TestPiece(unittest.TestCase):
    def setUp(self):
        self.mine_piece = Piece(True)
        self.empty_piece = Piece(False)
        self.neighbors = [Piece(True), Piece(False), Piece(False)]
        self.empty_piece.set_neighbours(self.neighbors)

    def test_initialization(self):
        self.assertTrue(self.mine_piece.get_has_mine())
        self.assertFalse(self.empty_piece.get_has_mine())
        self.assertFalse(self.mine_piece.get_revealed())
        self.assertFalse(self.empty_piece.get_revealed())
        self.assertFalse(self.mine_piece.get_flagged())
        self.assertFalse(self.empty_piece.get_flagged())
        self.assertEqual(self.mine_piece.get_num(), 0)

    def test_get_has_mine(self):
        # Testing that get_has_mine returns the correct value
        self.assertTrue(self.mine_piece.get_has_mine())
        self.assertFalse(self.empty_piece.get_has_mine())

    def test_get_revealed(self):
        # Testing that get_revealed returns the correct value
        self.assertFalse(self.mine_piece.get_revealed())
        self.mine_piece.click()
        self.assertTrue(self.mine_piece.get_revealed())

    def test_set_num(self):
        # Testing that set_num sets the correct value
        self.assertEqual(self.empty_piece.get_num(), 1)

    def test_get_flagged(self):
        # Testing that get_flagged returns the correct value
        self.assertFalse(self.mine_piece.get_flagged())
        self.mine_piece.set_flagged()
        self.assertTrue(self.mine_piece.get_flagged())