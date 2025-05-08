# pylint: disable=no-member
import os
import time
import pygame

class GameConfig:
    """Sisältää pelin käyttöliittymän resurssit"""

    def __init__(self):
        """Alustaa resurssit oletusarvoihin."""
        self.screen = None
        self.font = None
        self.menu_font = None
        self.images = {}

class GameUI:
    """Vastaa pelin käyttöliittymästä ja graafisista elementeistä."""

    def __init__(self, screen_size, piece_size):
        """Alustaa käyttöliittymän.

        Args:
            screen_size: tuple, näytön koko (leveys, korkeus).
            piece_size: tuple, ruutujen koko (leveys, korkeus).
        """
        self.screen_size = screen_size
        self.piece_size = piece_size
        pygame.init()
        pygame.font.init()
        self.config = GameConfig()
        self.config.font = pygame.font.SysFont('verdana', 48, bold=True)
        self.config.menu_font = pygame.font.SysFont('verdana', 36, bold=True)
        self.render_images()

    def draw_board(self, board, game_logic, images):
        """Piirtää pelilaudan ruudut näytölle."""
        topleft = (0,0)
        for row in range(board.get_size()[0]):
            for col in range(board.get_size()[1]):
                piece = board.get_piece((row, col))
                image_name = game_logic.get_image_name(piece)
                image = images[image_name]
                self.config.screen.blit(image, topleft)
                topleft = topleft[0]+ self.piece_size[0], topleft[1]
            topleft = 0, topleft[1] + self.piece_size[1]

    def draw_buttons(self, button_data, font=None, width=None, height=None):
        """Piirtää painikkeet näytölle.

        Args:
            button_data: Lista tupleja (Rect, teksti).
            font: Fontti tekstille, oletuksena self.config.menu_font.
            width: Painikkeen leveys, jos None käytetään Rect-olion leveyttä.
            height: Painikkeen korkeus, jos None käytetään Rect-olion korkeutta.

        Returns:
            list: Lista tupleja (Rect, teksti).
        """
        font = font or self.config.menu_font
        buttons = []

        for button, text in button_data:
            button_width = width or button.width
            button_height = height or button.height

            button_image = pygame.transform.scale(
                self.config.images['unopened'],
                (button_width, button_height)
            )
            self.config.screen.blit(button_image, button)

            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.config.screen.blit(text_surface, text_rect)

            buttons.append((button, text))

        return buttons

    def draw_menu_screen(self, buttons):
        """Piirtää päävalikon näytölle.

        Args:
            buttons: Sisältää painikkeiden Rect-oliot.
        """
        self.config.screen.fill((255, 255, 255))

        self.draw_menu_title()

        button_list = [
            (buttons["easy"], 'Easy'),
            (buttons["medium"], 'Medium'),
            (buttons["hard"], 'Hard'),
            (buttons["quit"], 'Quit')
        ]

        self.draw_buttons(
            button_list,
            width=buttons["width"],
            height=buttons["height"]
        )

        pygame.display.flip()

    def draw_menu_title(self):
        """Piirtää pelin otsikon ja miinojen kuvat päävalikkoon."""
        title = self.config.font.render('Minesweeper', True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.config.screen.get_width() / 2, 80))

        mine_size = (48, 48)
        mine_image = pygame.transform.scale(self.config.images['minex'], mine_size)

        left_mine_pos = (title_rect.left - mine_size[0] - 20, title_rect.centery - mine_size[1]//2)
        right_mine_pos = (title_rect.right + 20, title_rect.centery - mine_size[1]//2)

        self.config.screen.blit(title, title_rect)
        self.config.screen.blit(mine_image, left_mine_pos)
        self.config.screen.blit(mine_image, right_mine_pos)

    def draw_game_over_background(self, board, game_logic, images, config):
        """Piirtää pelin loppuvalikon taustan ja viestit."""
        self.draw_board(board, game_logic, images)

        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 180))
        self.config.screen.blit(overlay, (0, 0))

        title = config["title_font"].render(config["message"], True, config["color"])
        title_rect = title.get_rect(center=(self.screen_size[0]/2, config["message_y"]))
        self.config.screen.blit(title, title_rect)

        if config["won"]:
            time_text = f"Your time: {config['elapsed_time']:.2f}s"
            time_surface = config["time_font"].render(time_text, True, (255, 255, 255))
            time_rect = time_surface.get_rect(center=(self.screen_size[0]/2, config["time_y"]))
            self.config.screen.blit(time_surface, time_rect)

    def calculate_button_sizes(self):
        """Laskee loppuvalikon painikkeiden ja tekstien sijainnit ja koot.

        Returns:
            dict: Sisältää painikkeiden ja tekstien sijainnit ja koot.
        """
        button_width = min(200, self.screen_size[0] // 2)
        button_height = min(50, self.screen_size[1] // 10)
        button_x = self.screen_size[0] // 2 - button_width // 2

        message_y = self.screen_size[1] // 4
        time_y = message_y + 50
        retry_y = self.screen_size[1] * 0.6
        menu_y = retry_y + button_height * 1.2

        return {
            "width": button_width,
            "height": button_height,
            "x": button_x,
            "message_y": message_y,
            "time_y": time_y,
            "retry_y": retry_y,
            "menu_y": menu_y
        }

    def create_menu_buttons(self):
        """Luo päävalikon painikkeet.

        Returns:
            dict: Sisältää painikkeiden Rect-oliot ja niiden koot.
        """
        button_width = 200
        button_height = 50
        button_x = self.config.screen.get_width() // 2 - button_width // 2

        easy_button = pygame.Rect(button_x, 150, button_width, button_height)
        medium_button = pygame.Rect(button_x, 250, button_width, button_height)
        hard_button = pygame.Rect(button_x, 350, button_width, button_height)
        quit_button = pygame.Rect(button_x, 450, button_width, button_height)

        return {
            "easy": easy_button,
            "medium": medium_button,
            "hard": hard_button,
            "quit": quit_button,
            "width": button_width,
            "height": button_height
        }

    def create_game_over_buttons(self, sizes):
        """Luo pelin loppuvalikon painikkeet.

        Args:
            sizes: sisältää painikkeiden sijainnit ja koot.

        Returns:
            dict: Sisältää Rect-oliot retry- ja main menu -painikkeille.
        """
        retry_button = pygame.Rect(
            sizes["x"],
            sizes["retry_y"],
            sizes["width"],
            sizes["height"]
        )

        main_menu_button = pygame.Rect(
            sizes["x"],
            sizes["menu_y"],
            sizes["width"],
            sizes["height"]
        )

        return {
            "retry": retry_button,
            "main_menu": main_menu_button
        }

    def prepare_game_over_text(self, won):
        """Valmistelee pelin loppuvalikon tekstit ja fontit.

        Args:
            won: True jos pelaaja voitti.

        Returns:
            tuple: Palauttaa viestin, värit ja fontit.
        """
        message = "You Won!" if won else "You Lost!"
        colors = {
            "title": (0, 200, 0) if won else (255, 0, 0)
        }

        title_font_size = max(16, min(48, int(self.screen_size[1] / 10)))
        time_font_size = max(14, min(36, int(self.screen_size[1] / 12)))
        button_font_size = max(12, min(36, int(self.screen_size[1] / 15)))

        fonts = {
            "title": pygame.font.SysFont('verdana', title_font_size, bold=True),
            "time": pygame.font.SysFont('verdana', time_font_size, bold=True),
            "button": pygame.font.SysFont('verdana', button_font_size, bold=True)
        }

        return message, colors, fonts

    def render_images(self):
        """Lataa ja skaalaa pelissä käytettävät kuvat."""
        self.config.images = {}
        for filename in os.listdir("images"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(os.path.join("images", filename))
            image = pygame.transform.scale(image, self.piece_size)
            self.config.images[filename.split(".")[0]] = image

class GameLogic:
    """Pelin logiikasta ja tilanhallinnasta vastaava luokka."""

    def __init__(self, board):
        """Alustaa pelilogiikan.

        Args:
            board: Board-olio, joka sisältää pelilaudan.
        """
        self.board = board
        self.start_time = 0
        self.elapsed_time = 0

    def start_game(self):
        """Aloittaa pelin ajanlaskun."""
        self.start_time = time.time()

    def update_time(self):
        """Päivittää kuluneen ajan."""
        self.elapsed_time = time.time() - self.start_time
        return self.elapsed_time

    def handle_click(self, position, piece_size, flagging):
        """Käsittelee ruudun klikkauksen.

        Args:
            position: hiiren sijainti.
            piece_size: ruudun koko.
            flagging: True, jos lippua asetetaan.
        """
        if self.board.get_lost():
            return
        idx = position[1] // piece_size[1], position[0] // piece_size[0]
        piece = self.board.get_piece(idx)
        self.board.clicking(piece, flagging)

    def get_image_name(self, piece):
        """Palauttaa oikean kuvan nimen annetulle peliruudulle.

        Args:
            piece: Piece-olio.

        Returns:
            str: Kuvan nimi.
        """
        if piece.get_revealed():
            return "minered" if piece.has_mine else str(piece.get_num())
        return "flag" if piece.get_flagged() else "unopened"

class Game:
    """Pelin pääluokka. Yhdistää käyttöliittymän ja pelilogiikan."""

    def __init__(self, board, max_cell_size=50, menu_screen_size=(800, 800)):
        """Alustaa pelin.

        Args:
            board: Board-olio, joka sisältää pelilaudan.
            max_cell_size: Yksittäisen ruudun maksimikoko pikseleinä.
            menu_screen_size: tuple, päävalikon näytön koko (leveys, korkeus).
        """
        self.board = board
        self.max_cell_size = max_cell_size
        self.menu_screen_size = menu_screen_size

        board_size = self.board.get_size()

        self.piece_size = (self.max_cell_size, self.max_cell_size)
        self.screen_size = (
            board_size[1] * self.piece_size[0],
            board_size[0] * self.piece_size[1]
        )

        self.ui = GameUI(self.screen_size, self.piece_size)
        self.logic = GameLogic(board)

    def run(self):
        """Pelin pääsilmukka. Käsittelee tapahtumat, piirtää pelin ja tarkistaa pelin tilan."""
        self.ui.config.screen = pygame.display.set_mode((self.screen_size))
        pygame.display.set_caption("Minesweeper")
        self.logic.start_game()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    flagging = pygame.mouse.get_pressed()[2]
                    self.logic.handle_click(position, self.piece_size, flagging)

            elapsed = self.logic.update_time()
            pygame.display.set_caption(f"Minesweeper - Time: {elapsed:.2f}s")

            self.draw()
            pygame.display.flip()

            if self.board.get_won():
                return self.show_game_over_menu(True)

            if self.board.get_lost():
                return self.show_game_over_menu(False)

    def draw(self):
        """Piirtää pelilaudan."""
        self.ui.config.screen.fill((255, 255, 255))
        self.ui.draw_board(self.board, self.logic, self.ui.config.images)

    def main_menu(self):
        """Näyttää pelin päävalikon ja käsittelee käyttäjän syötteet.
        Palauttaa valitun pelilaudan asetukset tuple-muodossa.
        """
        self.ui.config.screen = pygame.display.set_mode(self.menu_screen_size)
        pygame.display.set_caption("Minesweeper - Main Menu")

        buttons = self.ui.create_menu_buttons()

        while True:
            self.ui.draw_menu_screen(buttons)
            result = self._handle_menu_events(buttons)
            if result is not None:
                return result

    def _handle_menu_events(self, buttons):
        """Käsittelee päävalikon tapahtumat.

        Args:
            buttons: sisältää painikkeiden Rect-oliot.

        Returns:
            Palauttaa pelilaudan asetukset tai None.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttons["easy"].collidepoint(mouse_pos):
                    return (8, 8, 0.1)
                if buttons["medium"].collidepoint(mouse_pos):
                    return (16, 16, 0.12)
                if buttons["hard"].collidepoint(mouse_pos):
                    return (32, 32, 0.15)
                if buttons["quit"].collidepoint(mouse_pos):
                    pygame.quit()
                    return None
        return None

    def show_game_over_menu(self, won):
        """Näyttää pelin loppuvalikon (voitit/hävisit).

        Args:
            won: True jos pelaaja voitti.

        Returns:
            Palauttaa "retry" tai "main_menu" käyttäjän valinnan mukaan.
        """
        button_sizes = self.ui.calculate_button_sizes()
        buttons = self.ui.create_game_over_buttons(button_sizes)
        message, colors, fonts = self.ui.prepare_game_over_text(won)

        config = {
            "message": message,
            "color": colors["title"],
            "title_font": fonts["title"],
            "time_font": fonts["time"],
            "button_font": fonts["button"],
            "message_y": button_sizes["message_y"],
            "time_y": button_sizes["time_y"],
            "buttons": buttons,
            "won": won,
            "elapsed_time": self.logic.elapsed_time
        }

        while True:
            self.ui.draw_game_over_background(self.board, self.logic, self.ui.config.images, config)

            button_data = [
                (config["buttons"]["retry"], "Retry"),
                (config["buttons"]["main_menu"], "Menu")
            ]
            buttons = self.ui.draw_buttons(button_data, font=config["button_font"])

            pygame.display.flip()

            result = self.handle_game_over_events(buttons)
            if result:
                return result

    def handle_game_over_events(self, buttons):
        """Käsittelee pelin loppuvalikon tapahtumat.

        Args:
            buttons: sisältää painikkeiden Rect-oliot.

        Returns:
            Palauttaa "retry", "main_menu", tai None riippuen käyttäjän valinnasta.
        """
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

