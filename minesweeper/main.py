from game import Game
from board import Board

def main():
    initial_size = (900, 900)  
    dummy_board = Board((8, 8), 0.1)
    game = Game(dummy_board, initial_size)
    
    settings = game.main_menu()
    if settings is None: 
        return
    
    size_x, size_y, prob = settings
    board_size = (size_x, size_y)
    screen_size = (min(size_x * 32, 900), min(size_y * 32, 900))  
    board = Board(board_size, prob)
    game = Game(board, screen_size)
    game.run()

if __name__ == "__main__":
    main()
