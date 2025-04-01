import pygame
import os

class Game():
    def __init__(self, board, screenSize):
        self.board = board
        self.screenSize = screenSize
        self.pieceSize = self.screenSize[0] // self.board.getSize()[1], self.screenSize[1] // self.board.getSize()[0]
        self.renderimages()

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
        idx = position[1] // self.pieceSize[1], position[0] // self.pieceSize[0]
        piece = self.board.getPiece(idx)
        self.board.clicking(piece, flagging)


