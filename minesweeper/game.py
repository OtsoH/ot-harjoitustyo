# pylint: disable=no-member
import os
import time
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
        self.menu_font = pygame.font.SysFont('verdana', 36, bold=True)
        self.render_images()
        self.start_time = 0
        self.elapsed_time = 0

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

    def show_game_over_menu(self, won):
        config = self._setup_game_over_config(won)

        while True:
            self._draw_game_over_background(config)
            buttons = self._draw_game_over_buttons(config)

            pygame.display.flip()

            result = self._handle_game_over_events(buttons)
            if result:
                return result

    def _setup_game_over_config(self, won):
        button_width = min(200, self.screen_size[0] // 2)
        button_height = min(50, self.screen_size[1] // 10)
        button_x = self.screen_size[0] // 2 - button_width // 2

        message_y = self.screen_size[1] // 4
        time_y = message_y + 50
        retry_y = self.screen_size[1] * 0.6
        menu_y = retry_y + button_height * 1.2

        retry_button = pygame.Rect(button_x, retry_y, button_width, button_height)
        main_menu_button = pygame.Rect(button_x, menu_y, button_width, button_height)

        message = "You Won!" if won else "You Lost!"
        color = (0, 200, 0) if won else (255, 0, 0)

        title_font_size = max(16, min(48, int(self.screen_size[1] / 10)))
        time_font_size = max(14, min(36, int(self.screen_size[1] / 12)))
        button_font_size = max(12, min(36, int(self.screen_size[1] / 15)))

        title_font = pygame.font.SysFont('verdana', title_font_size, bold=True)
        time_font = pygame.font.SysFont('verdana', time_font_size, bold=True)
        button_font = pygame.font.SysFont('verdana', button_font_size, bold=True)

        return {
            "message": message,
            "color": color,
            "title_font": title_font,
            "time_font": time_font,
            "button_font": button_font,
            "message_y": message_y,
            "time_y": time_y,
            "buttons": {
                "retry": retry_button,
                "main_menu": main_menu_button
            },
            "won": won,
            "elapsed_time": self.elapsed_time
        }

    def _draw_game_over_background(self, config):
        self.draw()

        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.screen.blit(overlay, (0, 0))

        title = config["title_font"].render(config["message"], True, config["color"])
        title_rect = title.get_rect(center=(self.screen_size[0]/2, config["message_y"]))
        self.screen.blit(title, title_rect)

        if config["won"]:
            time_text = f"Your time: {config['elapsed_time']:.2f}s"
            time_surface = config["time_font"].render(time_text, True, (255, 255, 255))
            time_rect = time_surface.get_rect(center=(self.screen_size[0]/2, config["time_y"]))
            self.screen.blit(time_surface, time_rect)

    def _draw_game_over_buttons(self, config):
        buttons = []

        button_data = [
            (config["buttons"]["retry"], "Retry"),
            (config["buttons"]["main_menu"], "Menu")
        ]

        for button, text in button_data:
            button_image = pygame.transform.scale(
                self.images['unopened'],
                (button.width, button.height)
            )
            self.screen.blit(button_image, button)

            text_surface = config["button_font"].render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)

            buttons.append((button, text))

        return buttons

    def _handle_game_over_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                retry_button = buttons[0][0]
                main_menu_button = buttons[1][0]

                if retry_button.collidepoint(mouse_pos):
                    return "retry"
                if main_menu_button.collidepoint(mouse_pos):
                    return "main_menu"

        return None

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
        self.start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    flagging = pygame.mouse.get_pressed()[2]
                    self.clicking(position, flagging)

            self.elapsed_time = time.time() - self.start_time
            pygame.display.set_caption(f"Minesweeper - Time: {self.elapsed_time:.2f}s")

            self.draw()
            pygame.display.flip()

            if self.board.get_won():
                return self.show_game_over_menu(True)

            if self.board.get_lost():
                return self.show_game_over_menu(False)

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
