import unittest
from board import Board
from piece import Piece

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board_size = (5, 5)
        self.prob = 0 
        self.board = Board(self.board_size, self.prob)
    
    #Testing that getNeighbours handles all board positions correctly
    def test_getNeighbours(self):
        center_neighbors = self.board.getNeighbours((2, 2))
        self.assertEqual(len(center_neighbors), 8)
        
        corner_neighbors = self.board.getNeighbours((0, 0))
        self.assertEqual(len(corner_neighbors), 3)
        
        edge_neighbors = self.board.getNeighbours((0, 2))
        self.assertEqual(len(edge_neighbors), 5)
        
        for piece in center_neighbors:
            self.assertIsInstance(piece, Piece)

if __name__ == '__main__':
    unittest.main()