import unittest
from board import Board
from piece import Piece

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board_size = (5, 5)
        self.prob = 0
        self.board = Board(self.board_size, self.prob)

    #Testing that the board is correctly initialized
    def test_initialization(self):
        self.assertEqual(self.board.size, self.board_size)
        self.assertEqual(self.board.prob, self.prob)
        self.assertFalse(self.board.get_lost())
        self.assertFalse(self.board.get_won())
        self.assertEqual(len(self.board.board), self.board_size[0])
        self.assertEqual(len(self.board.board[0]), self.board_size[1])

    #Testing that get_size returns the correct size of the board
    def test_get_size(self):
        self.assertEqual(self.board.get_size(), self.board_size)

    #Testing that get_piece returns the correct piece
    def test_get_piece(self):
        piece = self.board.get_piece((1, 1))
        self.assertIsInstance(piece, Piece)
        self.assertEqual(piece, self.board.board[1][1])

    #Testing that get_neighbours handles all board positions correctly
    def test_get_neighbours(self):
        center_neighbors = self.board.get_neighbours((2, 2))
        self.assertEqual(len(center_neighbors), 8)

        corner_neighbors = self.board.get_neighbours((0, 0))
        self.assertEqual(len(corner_neighbors), 3)

        edge_neighbors = self.board.get_neighbours((0, 2))
        self.assertEqual(len(edge_neighbors), 5)

        for piece in center_neighbors:
            self.assertIsInstance(piece, Piece)

    #Testing that clicking on an empty piece works
    def test_clicking_empty_piece(self):
        piece = self.board.get_piece((2, 2))
        self.board.clicking(piece, False)
        self.assertTrue(piece.get_revealed())
        self.assertFalse(self.board.get_lost())
        self.assertGreater(self.board.num_clicked, 0)

    #Testing that clicking on a revelead piece does nothing
    def test_clicking_revealed_piece(self):
        piece = self.board.get_piece((2, 2))
        self.board.clicking(piece, False)
        self.assertTrue(piece.get_revealed())
        initial_clicked = self.board.num_clicked
        self.board.clicking(piece, False)
        self.assertEqual(self.board.num_clicked, initial_clicked)

    #Testing that (left)clicking on a flagged piece doesnt work
    def test_clicking_flagged_piece(self):
        piece = self.board.get_piece((2, 2))
        self.board.clicking(piece, True)
        self.assertTrue(piece.get_flagged())
        self.board.clicking(piece, False)
        self.assertFalse(piece.get_revealed())

    #Testing that flagging/unflagging works correctly
    def test_flagging(self):
        piece = self.board.get_piece((2, 2))
        self.board.clicking(piece, True)
        self.assertTrue(piece.get_flagged())
        self.board.clicking(piece, True)
        self.assertFalse(piece.get_flagged())

    #Testing that clicking on an empty piece reveals neighbours correctly
    def test_auto_reveal(self):
        center_piece = self.board.get_piece((2, 2))
        self.board.clicking(center_piece, False)
        for neighbor in center_piece.get_neighbours():
            self.assertTrue(neighbor.get_revealed())

if __name__ == '__main__':
    unittest.main()