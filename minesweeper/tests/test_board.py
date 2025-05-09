import unittest
from board import Board
from piece import Piece

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board_size = (5, 5)
        self.num_mines = 5
        self.board = Board(self.board_size, self.num_mines)

    #Testing that the board is correctly initialized
    def test_initialization(self):
        self.assertEqual(self.board.size, self.board_size)
        self.assertFalse(self.board.get_lost())
        self.assertFalse(self.board.get_won())
        self.assertEqual(len(self.board.board), self.board_size[0])
        self.assertEqual(len(self.board.board[0]), self.board_size[1])
        self.assertEqual(self.board.num_non_mines, self.board_size[0] * self.board_size[1] - self.num_mines)

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
        piece = None
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                test_piece = self.board.get_piece((row, col))
                if not test_piece.get_has_mine():
                    piece = test_piece
                    break
            if piece:
                break

        self.assertIsNotNone(piece)
        self.assertFalse(piece.get_has_mine())
        self.assertFalse(piece.get_revealed())

        initial_clicked = self.board.num_clicked

        self.board.clicking(piece, False)

        self.assertTrue(piece.get_revealed())
        self.assertGreater(self.board.num_clicked, initial_clicked)
        self.assertFalse(self.board.get_lost())

    #Testing that clicking on a revealed piece does nothing
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
        test_board = Board(self.board_size, 0)
        center_piece = test_board.get_piece((2, 2))

        self.assertFalse(center_piece.get_has_mine())
        self.assertEqual(center_piece.get_num(), 0)

        test_board.clicking(center_piece, False)

        self.assertTrue(center_piece.get_revealed())

        for neighbor in test_board.get_neighbours((2, 2)):
            self.assertTrue(neighbor.get_revealed())

    #Testing that all pieces are revealed and numbers are removed when the game is won/lost
    def test_reveal_all(self):
        non_mine_piece = None
        for row in range(self.board_size[0]):
            for col in range(self.board_size[1]):
                test_piece = self.board.get_piece((row, col))
                if not test_piece.get_has_mine():
                    non_mine_piece = test_piece
                    break
            if non_mine_piece:
                break

        self.board.clicking(non_mine_piece, False)
        revealed_count_before = sum(piece.get_revealed() for row in self.board.board for piece in row)
        self.assertLess(revealed_count_before, self.board_size[0] * self.board_size[1])

        self.board.reveal_all()

        for row in self.board.board:
            for piece in row:
                self.assertTrue(piece.get_revealed())

        for row in self.board.board:
            for piece in row:
                if piece.get_has_mine():
                    self.assertEqual(piece.get_num(), 0)


