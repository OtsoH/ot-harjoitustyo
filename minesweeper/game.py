import pygame
import os

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        pygame.font.init()
        self.font = pygame.font.SysFont('verdana', 48, bold=True)
        self.menu_font = pygame.font.SysFont('verdana', 36)
        self.renderimages()

    def main_menu(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenSize))
        pygame.display.set_caption("Minesweeper - Main Menu")
        button_width = 200
        button_height = 50
        button_x = self.screenSize[0] // 2 - button_width // 2
        
        easy_button = pygame.Rect(button_x, 150, button_width, button_height)
        medium_button = pygame.Rect(button_x, 250, button_width, button_height)
        hard_button = pygame.Rect(button_x, 350, button_width, button_height)
        quit_button = pygame.Rect(button_x, 450, button_width, button_height)

        while True:
            self.screen.fill((255, 255, 255)) 
            
            title = self.font.render('Minesweeper', True, (255, 0, 0))
            title_rect = title.get_rect(center=(self.screenSize[0]/2, 80))
            
            mine_size = (48, 48) 
            mine_image = pygame.transform.scale(self.images['minex'], mine_size)
            
            left_mine_pos = (title_rect.left - mine_size[0] - 20, title_rect.centery - mine_size[1]//2)
            right_mine_pos = (title_rect.right + 20, title_rect.centery - mine_size[1]//2)
            
            self.screen.blit(title, title_rect)
            self.screen.blit(mine_image, left_mine_pos)
            self.screen.blit(mine_image, right_mine_pos)
            
            for button, text in [
                (easy_button, 'Easy'),
                (medium_button, 'Medium'),
                (hard_button, 'Hard'),
                (quit_button, 'Quit')
            ]:
                button_image = pygame.transform.scale(
                    self.images['unopened'], 
                    (button_width, button_height)
                )
                self.screen.blit(button_image, button)
                text_surface = self.menu_font.render(text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=button.center)
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        return (8, 8, 0.1)  
                    elif medium_button.collidepoint(mouse_pos):
                        return (16, 16, 0.15)
                    elif hard_button.collidepoint(mouse_pos):
                        return (32, 32, 0.2)
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        return None

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screenSize))
        pygame.display.set_caption("Minesweeper")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    flagging = pygame.mouse.get_pressed()[2]
                    self.clicking(position, flagging)
            self.draw()
            pygame.display.flip()
            if self.board.getwon():
                print("You won!")
                pygame.quit()
                return

    def draw(self):
        topleft = (0,0)
        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.getPiece((row, col))
                image = self.getImage(piece)
                self.screen.blit(image, topleft)
                topleft = topleft[0]+ self.pieceSize[0], topleft[1]
            topleft = 0, topleft[1] + self.pieceSize[1]

    def renderimages(self):
        self.images = {}
        for filename in os.listdir("images"):
            if (not filename.endswith(".png")):
                continue
            image = pygame.image.load(r"images/" + filename)
            image = pygame.transform.scale(image, self.pieceSize)
            self.images[filename.split(".")[0]] = image

    def getImage(self, piece):
        string = None
        if (piece.getrevealed()):
            string = "minered" if piece.hasMine else str(piece.getNum())
        else:
            string = "flag" if piece.getflagged() else "unopened"
        return self.images[string]
    
    def clicking(self, position, flagging):
        if (self.board.getlost()):
            return
        idx = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
        piece = self.board.getPiece(idx)
        self.board.clicking(piece, flagging)


