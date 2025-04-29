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

class Game():
    """Pelin pääluokka. Vastaa pelin tilasta, silmukasta ja käyttöliittymästä."""
    def __init__(self, board, screen_size):
        """Alustaa pelin.

        Args:
            board: Board-olio, joka sisältää pelilaudan.
            screen_size: tuple, näytön koko (leveys, korkeus).
        """
        self.board = board
        self.screen_size = screen_size
        self.piece_size = (
            self.screen_size[0] // self.board.get_size()[1],
            self.screen_size[1] // self.board.get_size()[0]
        )
        pygame.init()
        pygame.font.init()
        self.config = GameConfig()
        self.config.screen = None
        self.config.font = pygame.font.SysFont('verdana', 48, bold=True)
        self.config.menu_font = pygame.font.SysFont('verdana', 36, bold=True)
        self._render_images()
        self.start_time = 0
        self.elapsed_time = 0

    def main_menu(self):
        """Näyttää pelin päävalikon ja käsittelee käyttäjän syötteet.
        Palauttaa valitun pelilaudan asetukset tuple-muodossa.
        """
        self.config.screen = pygame.display.set_mode((self.screen_size))
        pygame.display.set_caption("Minesweeper - Main Menu")

        buttons = self._create_menu_buttons()

        while True:
            self._draw_menu_screen(buttons)
            result = self._handle_menu_events(buttons)
            if result is not None:
                return result

    def _create_menu_buttons(self):
        """Luo päävalikon painikkeet.

        Returns:
            dict: Sisältää painikkeiden Rect-oliot ja niiden koot.
        """
        button_width = 200
        button_height = 50
        button_x = self.screen_size[0] // 2 - button_width // 2

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

    def _draw_menu_screen(self, buttons):
        """Piirtää päävalikon näytölle.

        Args:
            buttons: Sisältää painikkeiden Rect-oliot.
        """
        self.config.screen.fill((255, 255, 255))

        self._draw_menu_title()

        button_list = [
            (buttons["easy"], 'Easy'),
            (buttons["medium"], 'Medium'),
            (buttons["hard"], 'Hard'),
            (buttons["quit"], 'Quit')
        ]

        self._draw_menu_buttons(
            button_list,
            buttons["width"],
            buttons["height"]
        )

        pygame.display.flip()

    def _draw_menu_title(self):
        """Piirtää pelin otsikon ja miinojen kuvat päävalikkoon."""

        title = self.config.font.render('Minesweeper', True, (255, 0, 0))
        title_rect = title.get_rect(center=(self.screen_size[0]/2, 80))

        mine_size = (48, 48)
        mine_image = pygame.transform.scale(self.config.images['minex'], mine_size)

        left_mine_pos = (
            title_rect.left - mine_size[0] - 20,
            title_rect.centery - mine_size[1]//2
        )
        right_mine_pos = (title_rect.right + 20, title_rect.centery - mine_size[1]//2)

        self.config.screen.blit(title, title_rect)
        self.config.screen.blit(mine_image, left_mine_pos)
        self.config.screen.blit(mine_image, right_mine_pos)

    def show_game_over_menu(self, won):
        """Näyttää pelin loppuvalikon (voitit/hävisit).

        Args:
            won: True jos pelaaja voitti.

        Returns:
            Palauttaa "retry" tai "main_menu" käyttäjän valinnan mukaan.
        """
        config = self._setup_game_over_config(won)

        while True:
            self._draw_game_over_background(config)
            buttons = self._draw_game_over_buttons(config)

            pygame.display.flip()

            result = self._handle_game_over_events(buttons)
            if result:
                return result

    def _setup_game_over_config(self, won):
        """Valmistelee pelin loppuvalikon asetukset.

        Args:
            won: True jos pelaaja voitti.

        Returns:
            dict: Sisältää viestit, fontit, värit ja painikkeet.
        """
        button_sizes = self._calculate_button_sizes()
        buttons = self._create_game_over_buttons(button_sizes)

        message, colors, fonts = self._prepare_game_over_text(won, button_sizes)

        return {
            "message": message,
            "color": colors["title"],
            "title_font": fonts["title"],
            "time_font": fonts["time"],
            "button_font": fonts["button"],
            "message_y": button_sizes["message_y"],
            "time_y": button_sizes["time_y"],
            "buttons": buttons,
            "won": won,
            "elapsed_time": self.elapsed_time
        }

    def _calculate_button_sizes(self):
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

    def _create_game_over_buttons(self, sizes):
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

    def _prepare_game_over_text(self, won, _):
        """Valmistelee pelin loppuvalikon tekstit ja fontit.

        Args:
            won: True jos pelaaja voitti.
            _: Käyttämätön parametri.

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

    def _draw_game_over_background(self, config):
        """Piirtää pelin loppuvalikon taustan ja viestit.

        Args:
            config: Sisältää viestit, fontit, värit ja painikkeet.
        """
        self._draw()

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

    def _draw_game_over_buttons(self, config):
        """Piirtää pelin loppuvalikon painikkeet.

        Args:
            config: sisältää painikkeiden Rect-oliot ja fontit.

        Returns:
            list: Sisältää tupleja painikkeista.
        """
        buttons = []

        button_data = [
            (config["buttons"]["retry"], "Retry"),
            (config["buttons"]["main_menu"], "Menu")
        ]

        for button, text in button_data:
            button_image = pygame.transform.scale(
                self.config.images['unopened'],
                (button.width, button.height)
            )
            self.config.screen.blit(button_image, button)

            text_surface = config["button_font"].render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.config.screen.blit(text_surface, text_rect)

            buttons.append((button, text))

        return buttons

    def _handle_game_over_events(self, buttons):
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

    def _draw_menu_buttons(self, buttons, button_width, button_height):
        """Piirtää päävalikon painikkeet.

        Args:
            buttons: list, sisältää tupleja (Rect, teksti).
            button_width: int, painikkeen leveys.
            button_height: int, painikkeen korkeus.
        """
        for button, text in buttons:
            button_image = pygame.transform.scale(
                self.config.images['unopened'],
                (button_width, button_height)
            )
            self.config.screen.blit(button_image, button)
            text_surface = self.config.menu_font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.config.screen.blit(text_surface, text_rect)

    def run(self):
        """Pelin pääsilmukka. Käsittelee tapahtumat, piirtää pelin ja tarkistaa pelin tilan."""

        self.config.screen = pygame.display.set_mode((self.screen_size))
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
                    self._clicking(position, flagging)

            self.elapsed_time = time.time() - self.start_time
            pygame.display.set_caption(f"Minesweeper - Time: {self.elapsed_time:.2f}s")

            self._draw()
            pygame.display.flip()

            if self.board.get_won():
                return self.show_game_over_menu(True)

            if self.board.get_lost():
                return self.show_game_over_menu(False)

    def _draw(self):
        """Piirtää pelilaudan ruudut näytölle."""

        topleft = (0,0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece((row, col))
                image = self._get_image(piece)
                self.config.screen.blit(image, topleft)
                topleft = topleft[0]+ self.piece_size[0], topleft[1]
            topleft = 0, topleft[1] + self.piece_size[1]

    def _render_images(self):
        """Lataa ja skaalaa pelissä käytettävät kuvat."""

        self.config.images = {}
        for filename in os.listdir("images"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(r"images/" + filename)
            image = pygame.transform.scale(image, self.piece_size)
            self.config.images[filename.split(".")[0]] = image

    def _get_image(self, piece):
        """Palauttaa oikean kuvan annetulle peliruudulle.

        Args:
            piece: Piece-olio.

        Returns:
            Palauttaa ruudun kuvan.
        """
        string = None
        if piece.get_revealed():
            string = "minered" if piece.has_mine else str(piece.get_num())
        else:
            string = "flag" if piece.get_flagged() else "unopened"
        return self.config.images[string]

    def _clicking(self, position, flagging):
        """Käsittelee ruudun klikkauksen.

        Args:
            position: hiiren sijainti.
            flagging: True, jos lippua asetetaan.
        """
        if self.board.get_lost():
            return
        idx = position[1] // self.piece_size[1], position[0] // self.piece_size[0]
        piece = self.board.get_piece(idx)
        self.board.clicking(piece, flagging)
