# pylint: disable=no-member
# pylint: disable=too-many-locals,too-many-statements
import os
import pygame

class Game():
    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size
        self.piece_size = (
            self.screen_size[0] // self.board.get_size()[1],
            self.screen_size[1] // self.board.get_size()[0]
        )
        pygame.init()
        pygame.font.init()
        self.screen = None
        self.font = pygame.font.SysFont('verdana', 48, bold=True)
        self.menu_font = pygame.font.SysFont('verdana', 36)
        self.render_images()

    def main_menu(self):
        self.screen = pygame.display.set_mode((self.screen_size))
        pygame.display.set_caption("Minesweeper - Main Menu")
        button_width = 200
        button_height = 50
        button_x = self.screen_size[0] // 2 - button_width // 2

        easy_button = pygame.Rect(button_x, 150, button_width, button_height)
        medium_button = pygame.Rect(button_x, 250, button_width, button_height)
        hard_button = pygame.Rect(button_x, 350, button_width, button_height)
        quit_button = pygame.Rect(button_x, 450, button_width, button_height)

        while True:
            self.screen.fill((255, 255, 255))

            title = self.font.render('Minesweeper', True, (255, 0, 0))
            title_rect = title.get_rect(center=(self.screen_size[0]/2, 80))

            mine_size = (48, 48)
            mine_image = pygame.transform.scale(self.images['minex'], mine_size)

            left_mine_pos = (
                title_rect.left - mine_size[0] - 20,
                title_rect.centery - mine_size[1]//2
            )
            right_mine_pos = (title_rect.right + 20, title_rect.centery - mine_size[1]//2)

            self.screen.blit(title, title_rect)
            self.screen.blit(mine_image, left_mine_pos)
            self.screen.blit(mine_image, right_mine_pos)

            self._draw_menu_buttons(
                [(easy_button, 'Easy'),
                 (medium_button, 'Medium'),
                 (hard_button, 'Hard'),
                 (quit_button, 'Quit')],
                button_width, button_height
            )

            pygame.display.flip()

            result = self._handle_menu_events(easy_button, medium_button, hard_button, quit_button)
            if result is not None:
                return result

    def _handle_menu_events(self, easy_button, medium_button, hard_button, quit_button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_pos):
                    return (8, 8, 0.1)
                if medium_button.collidepoint(mouse_pos):
                    return (16, 16, 0.12)
                if hard_button.collidepoint(mouse_pos):
                    return (32, 32, 0.15)
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    return None
        return None

    def _draw_menu_buttons(self, buttons, button_width, button_height):
        for button, text in buttons:
            button_image = pygame.transform.scale(
                self.images['unopened'],
                (button_width, button_height)
            )
            self.screen.blit(button_image, button)
            text_surface = self.menu_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)

    def run(self):
        self.screen = pygame.display.set_mode((self.screen_size))
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
            if self.board.get_won():
                print("You won!")
                pygame.quit()
                return

    def draw(self):
        topleft = (0,0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                image = self.get_image(piece)
                self.screen.blit(image, topleft)
                topleft = topleft[0]+ self.piece_size[0], topleft[1]
            topleft = 0, topleft[1] + self.piece_size[1]

    def render_images(self):
        self.images = {}
        for filename in os.listdir("images"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"images/" + filename)
            image = pygame.transform.scale(image, self.piece_size)
            self.images[filename.split(".")[0]] = image

    def get_image(self, piece):
        string = None
        if piece.get_revealed():
            string = "minered" if piece.has_mine else str(piece.get_num())
        else:
            string = "flag" if piece.get_flagged() else "unopened"
        return self.images[string]

    def clicking(self, position, flagging):
        if self.board.get_lost():
            return
        idx = position[1] // self.piece_size[1], position[0] // self.piece_size[0]
        piece = self.board.get_piece(idx)
        self.board.clicking(piece, flagging)
