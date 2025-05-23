# pylint: disable=no-member
import os
import time
import pygame

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
        self.screen = None
        self.font = pygame.font.SysFont('verdana', 48, bold=True)
        self.menu_font = pygame.font.SysFont('verdana', 36, bold=True)
        self.images = {}
        self.render_images()

    def render_images(self):
        """Lataa ja skaalaa pelissä käytettävät kuvat."""
        self.images = {}
        for filename in os.listdir("images"):
            if not filename.endswith(".png"):
                continue
            image = pygame.image.load(os.path.join("images", filename))
            image = pygame.transform.scale(image, self.piece_size)
            self.images[filename.split(".")[0]] = image

    def draw_board(self, board, game_logic, images):
        """Piirtää pelilaudan ruudut näytölle."""
        topleft = (0,0)
        for row in range(board.get_size()[0]):
            for col in range(board.get_size()[1]):
                piece = board.get_piece((row, col))
                image_name = game_logic.get_image_name(piece)
                image = images[image_name]
                self.screen.blit(image, topleft)
                topleft = topleft[0]+ self.piece_size[0], topleft[1]
            topleft = 0, topleft[1] + self.piece_size[1]

    def draw_buttons(self, button_data, font=None, width=None, height=None):
        """Piirtää painikkeet näytölle.

        Args:
            button_data: Lista tupleja (Rect, teksti).
            font: Fontti tekstille, oletuksena self.menu_font.
            width: Painikkeen leveys, jos None käytetään Rect-olion leveyttä.
            height: Painikkeen korkeus, jos None käytetään Rect-olion korkeutta.

        Returns:
            list: Lista tupleja (Rect, teksti).
        """
        font = font or self.menu_font
        buttons = []

        for button, text in button_data:
            button_width = width or button.width
            button_height = height or button.height

            button_image = pygame.transform.scale(
                self.images['unopened'],
                (button_width, button_height)
            )
            self.screen.blit(button_image, button)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button.center)
            self.screen.blit(text_surface, text_rect)

            buttons.append((button, text))

        return buttons

    def draw_menu_screen(self, buttons):
        """Piirtää päävalikon näytölle.

        Args:
            buttons: Sisältää painikkeiden Rect-oliot.
        """
        self.screen.fill((255, 255, 255))

        self.draw_title('Minesweeper', 'minex', (255, 0, 0))

        button_list = [
            (buttons["easy"], 'Easy'),
            (buttons["medium"], 'Medium'),
            (buttons["hard"], 'Hard'),
            (buttons["custom"], 'Custom'),
            (buttons["quit"], 'Quit')
        ]

        self.draw_buttons(
            button_list,
            width=buttons["width"],
            height=buttons["height"]
        )

    def draw_title(self, title_text, icon_name="minex", color=(255, 0, 0)):
        """Piirtää pelin otsikon ja kuvat sen molemmin puolin."""
        title = self.font.render(title_text, True, color)
        title_rect = title.get_rect(center=(self.screen.get_width() / 2, 80))

        icon_size = (48, 48)
        icon_image = pygame.transform.scale(self.images[icon_name], icon_size)

        left_icon_pos = (title_rect.left - icon_size[0] - 20, title_rect.centery - icon_size[1]//2)
        right_icon_pos = (title_rect.right + 20, title_rect.centery - icon_size[1]//2)

        self.screen.blit(title, title_rect)
        self.screen.blit(icon_image, left_icon_pos)
        self.screen.blit(icon_image, right_icon_pos)

    def draw_game_over_background(self, config):
        """Piirtää pelin loppuvalikon taustan ja viestit.

        Args:
            config: Sanakirja, joka sisältää:
                - message: Näytettävä viesti ("You Won!" tai "You Lost!")
                - color: Viestin väri
                - title_font: Otsikon fontti
                - time_font: Ajan näyttämiseen käytettävä fontti
                - message_y: Viestin y-koordinaatti
                - time_y: Ajan y-koordinaatti
                - won: True jos pelaaja voitti
                - elapsed_time: Peliin kulunut aika
                - board: Pelilauta (Board-olio)
                - logic: Pelilogiikka (GameLogic-olio)
        """
        self.draw_board(config["board"], config["logic"], self.images)

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
        button_x = self.screen.get_width() // 2 - button_width // 2

        easy_button = pygame.Rect(button_x, 150, button_width, button_height)
        medium_button = pygame.Rect(button_x, 230, button_width, button_height)
        hard_button = pygame.Rect(button_x, 310, button_width, button_height)
        custom_button = pygame.Rect(button_x, 390, button_width, button_height)
        quit_button = pygame.Rect(button_x, 470, button_width, button_height)

        return {
            "easy": easy_button,
            "medium": medium_button,
            "hard": hard_button,
            "custom": custom_button,
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

    #Generoitu koodi alkaa
    def draw_slider(self, value, min_value, max_value, slider_rect, slider_color=(200, 200, 200),
                    handle_color=(255, 0, 0), label=None, label_color=(255, 0, 0)):
        """Piirtää liukusäätimen ja sen kahvan.

        Args:
            value: Liukusäätimen nykyinen arvo
            min_value: Liukusäätimen minimiarvo
            max_value: Liukusäätimen maksimiarvo
            slider_rect: Liukusäätimen Rect-olio (tausta)
            slider_color: Liukusäätimen taustan väri, oletuksena (200, 200, 200)
            handle_color: Liukusäätimen kahvan väri, oletuksena (255, 0, 0)
            label: Liukusäätimen otsikko, esim. "Size: 15x15"
            label_color: Otsikon väri, oletuksena (255, 0, 0)

        Returns:
            pygame.Rect: Palauttaa liukusäätimen kahvan Rect-olion.
        """
        pygame.draw.rect(self.screen, slider_color, slider_rect)

        pygame.draw.rect(self.screen, (0, 0, 0), slider_rect, 2)

        handle_x = slider_rect.left + ((value - min_value) / (max_value - min_value)) * slider_rect.width

        handle_height = slider_rect.height + 10
        handle_rect = pygame.Rect(handle_x - 5, slider_rect.top - 5, 10, handle_height)
        pygame.draw.rect(self.screen, handle_color, handle_rect)

        if label:
            label_surface = self.menu_font.render(label, True, label_color)
            self.screen.blit(label_surface, (slider_rect.left, slider_rect.top - 40))

        return handle_rect

    def create_slider(self, name, x, y, width, height, min_value, max_value, initial_value):
        """Luo liukusäätimen määritettyjen parametrien mukaan.

        Args:
            name: Liukusäätimen nimi (tunniste)
            x: Liukusäätimen x-koordinaatti
            y: Liukusäätimen y-koordinaatti
            width: Liukusäätimen leveys
            height: Liukusäätimen korkeus
            min_value: Liukusäätimen minimiarvo
            max_value: Liukusäätimen maksimiarvo
            initial_value: Liukusäätimen alkuarvo

        Returns:
            dict: Sisältää liukusäätimen tiedot:
                - rect: Liukusäätimen Rect-olio
                - min_value: Minimiarvo
                - max_value: Maksimiarvo
                - value: Nykyinen arvo
                - width: Leveys
                - height: Korkeus
        """
        slider_rect = pygame.Rect(x, y, width, height)

        return {
            "name": name,
            "rect": slider_rect,
            "min_value": min_value,
            "max_value": max_value,
            "value": initial_value,
            "width": width,
            "height": height
        }
    #Generoitu koodi loppuu

    def draw_custom_game(self, game_settings):
        """Piirtää custom game -asetusikkunan käyttöliittymän.

        Args:
            game_settings: Sanakirja, joka sisältää:
                - rows_value: Pelilaudan rivien määrä
                - cols_value: Pelilaudan sarakkeiden määrä
                - mines_value: Miinojen määrä
                - min_size: Pienin sallittu koko
                - max_size: Suurin sallittu koko
                - max_mines: Suurin sallittu miinojen määrä
                - rows_slider: Rivien liukusäätimen Rect-olio
                - cols_slider: Sarakkeiden liukusäätimen Rect-olio
                - mines_slider: Miinojen liukusäätimen Rect-olio
                - ok_button: OK-painikkeen Rect-olio
                - back_button: Back-painikkeen Rect-olio
                - slider_width: Liukusäätimen leveys
                - slider_height: Liukusäätimen korkeus
        """
        self.screen.fill((255, 255, 255))

        self.draw_title('Custom Game', 'questionmark', (255, 0, 0))

        rows_text = f"Rows: {game_settings['rows_value']}"
        cols_text = f"Columns: {game_settings['cols_value']}"
        mines_text = f"Mines: {game_settings['mines_value']}"

        self.draw_slider(
            game_settings['rows_value'], game_settings['min_size'], game_settings['max_size'],
            game_settings['rows_slider'], label=rows_text, label_color=(255, 0, 0)
        )

        self.draw_slider(
            game_settings['cols_value'], game_settings['min_size'], game_settings['max_size'],
            game_settings['cols_slider'], label=cols_text, label_color=(255, 0, 0)
        )

        self.draw_slider(
            game_settings['mines_value'], 1, game_settings['max_mines'],
            game_settings['mines_slider'], label=mines_text, label_color=(255, 0, 0)
        )

        button_data = [
            (game_settings['ok_button'], 'OK'),
            (game_settings['back_button'], 'Back')
        ]
        self.draw_buttons(button_data)

        pygame.display.flip()

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
            if piece.get_has_mine():
                return "minered" if piece == self.board.clicked_mine else "mine"
            return str(piece.get_num())
        return "flag" if piece.get_flagged() else "unopened"

class Game:
    """Pelin pääluokka. Yhdistää käyttöliittymän ja pelilogiikan."""
    def __init__(self, board, max_piece_size=50, menu_screen_size=(800, 800), db=None):
        """Alustaa pelin.

        Args:
            board: Board-olio, joka sisältää pelilaudan.
            max_piece_size: Yksittäisen ruudun maksimikoko pikseleinä.
            menu_screen_size: tuple, päävalikon näytön koko (leveys, korkeus).
            db: GameDatabase-instanssi.
        """
        self.board = board
        self.max_piece_size = max_piece_size
        self.menu_screen_size = menu_screen_size
        self.db = db

        board_size = self.board.get_size()

        self.piece_size = (self.max_piece_size, self.max_piece_size)
        self.screen_size = (
            board_size[1] * self.piece_size[0],
            board_size[0] * self.piece_size[1]
        )

        self.ui = GameUI(self.screen_size, self.piece_size)
        self.logic = GameLogic(board)
        self.custom_game = CustomGame(self.menu_screen_size, self.ui)

        self.difficulty_settings = {
            "easy": {"size": (9, 9), "mines": 10, "name": "Easy"},
            "medium": {"size": (16, 16), "mines": 40, "name": "Medium"},
            "hard": {"size": (16, 30), "mines": 99, "name": "Hard"}
        }

    def run(self):
        """Pelin pääsilmukka. Käsittelee tapahtumat, piirtää pelin ja tarkistaa pelin tilan."""
        self.ui.screen = pygame.display.set_mode((self.screen_size))
        pygame.display.set_caption("Minesweeper")
        self.logic.start_game()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if event.button == 1:
                        flagging = False
                        self.logic.handle_click(position, self.piece_size, flagging)
                    elif event.button == 3:
                        flagging = True
                        self.logic.handle_click(position, self.piece_size, flagging)

            elapsed = self.logic.update_time()
            pygame.display.set_caption(f"Minesweeper - Time: {elapsed:.2f}s")

            self.draw()
            pygame.display.flip()

            if self.board.get_won():
                self.board.reveal_all()
                return self.show_game_over_menu(True)

            if self.board.get_lost():
                self.board.reveal_all()
                return self.show_game_over_menu(False)

    def draw(self):
        """Piirtää pelilaudan."""
        self.ui.screen.fill((255, 255, 255))
        self.ui.draw_board(self.board, self.logic, self.ui.images)

    def main_menu(self):
        """Näyttää pelin päävalikon ja käsittelee käyttäjän syötteet."""
        self.ui.screen = pygame.display.set_mode(self.menu_screen_size)
        pygame.display.set_caption("Minesweeper - Main Menu")

        buttons = self.ui.create_menu_buttons()
        self.ui.draw_menu_screen(buttons)
        if self.db:
            self.prepare_and_display_highscores(buttons)
        pygame.display.flip()

        clock = pygame.time.Clock()
        need_redraw = False

        while True:
            need_redraw = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    need_redraw = True
                    mouse_pos = pygame.mouse.get_pos()

                    if buttons["easy"].collidepoint(mouse_pos):
                        return (9, 9, 10)
                    if buttons["medium"].collidepoint(mouse_pos):
                        return (16, 16, 40)
                    if buttons["hard"].collidepoint(mouse_pos):
                        return (16, 30, 99)
                    if buttons["custom"].collidepoint(mouse_pos):
                        custom_game = CustomGame(self.menu_screen_size, self.ui)
                        custom_settings = custom_game.show_settings()
                        if custom_settings is None:
                            continue
                        else:
                            return custom_settings
                    if buttons["quit"].collidepoint(mouse_pos):
                        pygame.quit()
                        return None

            if need_redraw:
                self.ui.draw_menu_screen(buttons)
                if self.db:
                    self.prepare_and_display_highscores(buttons)
                pygame.display.flip()
            clock.tick(30)

    def prepare_all_highscores(self):
        """Valmistelee high score -tekstit kaikille vaikeustasoille."""
        if not hasattr(self, 'highscore_surfaces'):
            self.highscore_surfaces = {}

        for difficulty in ["Easy", "Medium", "Hard"]:
            scores = self.db.get_high_scores(difficulty, limit=1)

            surface_width = 180
            surface_height = 30

            surface = pygame.Surface((surface_width, surface_height), pygame.SRCALPHA)
            surface.fill((255, 255, 255, 180))
            score_font = pygame.font.SysFont('verdana', 20, bold=True)

            if not scores:
                no_scores = score_font.render("Not completed", True, (255, 0, 0))
                no_scores_rect = no_scores.get_rect(center=(surface_width//2, surface_height//2))
                surface.blit(no_scores, no_scores_rect)
            else:
                time_value = scores[0][0]
                score_text = score_font.render(f"Best: {time_value:.2f}s", True, (0, 200, 0))
                score_rect = score_text.get_rect(center=(surface_width//2, surface_height//2))
                surface.blit(score_text, score_rect)

            self.highscore_surfaces[difficulty] = surface

    def display_all_highscores(self, buttons):
        """Näyttää high score -tekstit kaikkien vaikeustasojen vieressä."""
        self.ui.screen.blit(
            self.highscore_surfaces["Easy"],
            (buttons["easy"].right + 10, buttons["easy"].centery - self.highscore_surfaces["Easy"].get_height()//2)
        )
        self.ui.screen.blit(
            self.highscore_surfaces["Medium"],
            (buttons["medium"].right + 10, buttons["medium"].centery - self.highscore_surfaces["Medium"].get_height()//2)
        )

        self.ui.screen.blit(
            self.highscore_surfaces["Hard"],
            (buttons["hard"].right + 10, buttons["hard"].centery - self.highscore_surfaces["Hard"].get_height()//2)
        )

    def prepare_and_display_highscores(self, buttons):
        """Varmistaa, että high score -tiedot on valmisteltu ja näyttää ne."""
        if not self.db:
            return

        if not hasattr(self, 'highscore_surfaces'):
            self.prepare_all_highscores()

        self.display_all_highscores(buttons)

    def show_game_over_menu(self, won):
        """Näyttää pelin loppuvalikon (voitit/hävisit)."""
        button_sizes = self.ui.calculate_button_sizes()
        buttons = self.ui.create_game_over_buttons(button_sizes)
        message, colors, fonts = self.ui.prepare_game_over_text(won)

        if won and self.db:
            difficulty = self.get_current_difficulty()
            if difficulty:
                self.db.save_score(difficulty, self.logic.elapsed_time)
                if hasattr(self, 'highscore_surfaces'):
                    self.prepare_all_highscores()

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
            "elapsed_time": self.logic.elapsed_time,
            "board": self.board,
            "logic": self.logic
        }

        while True:
            self.ui.draw_game_over_background(config)

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

    def get_current_difficulty(self):
        """Määrittää nykyisen vaikeustason pelilaudan koon ja miinojen määrän perusteella.

        Returns:
            str: Vaikeustason nimi ("Easy", "Medium", "Hard") tai None jos Custom Game
        """
        board_size = self.board.get_size()
        mine_count = self.board.size[0] * self.board.size[1] - self.board.num_non_mines

        for _, settings in self.difficulty_settings.items():
            if (board_size == settings["size"] and mine_count == settings["mines"]):
                return settings["name"]

        return None

class CustomGame:
    """Vastaa custom-peliasetuksien käsittelystä."""
    def __init__(self, menu_screen_size, ui):
        """Alustaa custom-pelivalikon.

        Args:
            menu_screen_size: tuple, päävalikon näytön koko.
            ui: GameUI-olio, joka vastaa UI-elementtien piirtämisestä.
        """
        self.menu_screen_size = menu_screen_size
        self.ui = ui

    def show_settings(self):
        """Näyttää custom-peliasetukset ja käsittelee käyttäjän syötteet.

        Returns:
            tuple (rivit, sarakkeet, miinojen määrä) tai None.
        """
        original_screen = self.ui.screen.copy()

        min_size = 5
        max_size = 50
        initial_rows = 15
        initial_cols = 15
        initial_mines = 30

        slider_width = 300
        slider_height = 20
        slider_x = self.menu_screen_size[0] // 2 - slider_width // 2

        rows_slider = self.ui.create_slider("rows", slider_x, 150, slider_width, slider_height,
                                           min_size, max_size, initial_rows)
        cols_slider = self.ui.create_slider("cols", slider_x, 220, slider_width, slider_height,
                                           min_size, max_size, initial_cols)
        mines_slider = self.ui.create_slider("mines", slider_x, 290, slider_width, slider_height,
                                            1, initial_rows * initial_cols - 1, initial_mines)

        ok_button = pygame.Rect(self.menu_screen_size[0]//2 - 100, 370, 200, 50)
        back_button = pygame.Rect(self.menu_screen_size[0]//2 - 100, 440, 200, 50)

        active_slider = None

        rows_value = initial_rows
        cols_value = initial_cols
        mines_value = initial_mines
        max_mines = rows_value * cols_value - 1

        game_settings = {
            'rows_value': rows_value,
            'cols_value': cols_value,
            'mines_value': mines_value,
            'min_size': min_size,
            'max_size': max_size,
            'max_mines': max_mines,
            'rows_slider': rows_slider["rect"],
            'cols_slider': cols_slider["rect"],
            'mines_slider': mines_slider["rect"],
            'ok_button': ok_button,
            'back_button': back_button,
            'slider_width': slider_width,
            'slider_height': slider_height
        }

        while True:
            game_settings['max_mines'], game_settings['mines_value'] = self.update_ui(game_settings)

            rows_slider["value"] = game_settings['rows_value']
            cols_slider["value"] = game_settings['cols_value']
            mines_slider["value"] = game_settings['mines_value']
            mines_slider["max_value"] = game_settings['max_mines']

            result = self.handle_events(original_screen, game_settings, active_slider)

            if result is None:
                continue

            action, values = result

            if action == "update":
                game_settings['rows_value'] = values["rows_value"]
                game_settings['cols_value'] = values["cols_value"]
                game_settings['mines_value'] = values["mines_value"]
                active_slider = values["active_slider"]
            elif action == "ok":
                return values
            elif action == "back":
                return None

    def update_ui(self, game_settings):
        """Päivittää custom game -ikkunan käyttöliittymän tilan.

        Args:
            game_settings: Sanakirja, joka sisältää asetukset.

        Returns:
            tuple: (max_mines, mines_value)
        """
        max_mines = max(1, game_settings['rows_value'] * game_settings['cols_value'] - 1)
        mines_value = min(game_settings['mines_value'], max_mines)

        self.ui.draw_custom_game(game_settings)

        return max_mines, mines_value

    def handle_events(self, original_screen, game_settings, active_slider):
        """Käsittelee custom game -ikkunan tapahtumat."""
        handles = self._create_slider_handles(game_settings)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return self._handle_mouse_down(event, original_screen, game_settings, handles)

            elif event.type == pygame.MOUSEBUTTONUP:
                return self._handle_mouse_up(game_settings)

            elif event.type == pygame.MOUSEMOTION:
                if active_slider:
                    return self._handle_mouse_motion(event, game_settings, active_slider)

        return None

    #Generoitu koodi alkaa
    def _create_slider_handles(self, game_settings):
        """Luo liukusäätimien kahvat.

        Args:
            game_settings: Sanakirja, joka sisältää asetukset.

        Returns:
            dict: Liukusäätimien kahvat
        """
        rows_value = game_settings['rows_value']
        cols_value = game_settings['cols_value']
        mines_value = game_settings['mines_value']
        min_size = game_settings['min_size']
        max_size = game_settings['max_size']
        max_mines = game_settings['max_mines']
        rows_slider = game_settings['rows_slider']
        cols_slider = game_settings['cols_slider']
        mines_slider = game_settings['mines_slider']
        slider_width = game_settings['slider_width']
        slider_height = game_settings['slider_height']

        rows_handle_x = rows_slider.left + (rows_value - min_size) / (max_size - min_size) * slider_width
        cols_handle_x = cols_slider.left + (cols_value - min_size) / (max_size - min_size) * slider_width
        mines_handle_x = mines_slider.left + (mines_value / max_mines) * slider_width

        rows_handle = pygame.Rect(rows_handle_x - 5, rows_slider.top - 5, 10, slider_height + 10)
        cols_handle = pygame.Rect(cols_handle_x - 5, cols_slider.top - 5, 10, slider_height + 10)
        mines_handle = pygame.Rect(mines_handle_x - 5, mines_slider.top - 5, 10, slider_height + 10)

        return {
            "rows": rows_handle,
            "cols": cols_handle,
            "mines": mines_handle
        }

    def _handle_mouse_down(self, event, original_screen, game_settings, handles):
        """Käsittelee hiiren painallustapahtumat.

        Args:
            event: Pygame-tapahtuma
            original_screen: Alkuperäinen näyttö
            game_settings: Sanakirja, joka sisältää asetukset
            handles: Liukusäätimien kahvat

        Returns:
            tuple: (action, values) tai None
        """
        mouse_pos = event.pos
        rows_value = game_settings['rows_value']
        cols_value = game_settings['cols_value']
        mines_value = game_settings['mines_value']
        min_size = game_settings['min_size']
        max_size = game_settings['max_size']
        max_mines = game_settings['max_mines']
        rows_slider = game_settings['rows_slider']
        cols_slider = game_settings['cols_slider']
        mines_slider = game_settings['mines_slider']
        ok_button = game_settings['ok_button']
        back_button = game_settings['back_button']
        slider_width = game_settings['slider_width']

        if handles["rows"].collidepoint(mouse_pos):
            return ("update", {"active_slider": "rows", "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})
        elif handles["cols"].collidepoint(mouse_pos):
            return ("update", {"active_slider": "cols", "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})
        elif handles["mines"].collidepoint(mouse_pos):
            return ("update", {"active_slider": "mines", "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})

        elif rows_slider.collidepoint(mouse_pos):
            new_rows_value = self._calculate_slider_value(mouse_pos[0], rows_slider.left,
                                                         slider_width, min_size, max_size)
            return ("update", {"active_slider": "rows", "rows_value": new_rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})
        elif cols_slider.collidepoint(mouse_pos):
            new_cols_value = self._calculate_slider_value(mouse_pos[0], cols_slider.left,
                                                         slider_width, min_size, max_size)
            return ("update", {"active_slider": "cols", "rows_value": rows_value,
                              "cols_value": new_cols_value, "mines_value": mines_value})
        elif mines_slider.collidepoint(mouse_pos):
            new_mines_value = int((mouse_pos[0] - mines_slider.left) / slider_width * max_mines)
            new_mines_value = max(1, min(max_mines, new_mines_value))
            return ("update", {"active_slider": "mines", "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": new_mines_value})

        elif ok_button.collidepoint(mouse_pos):
            self.ui.screen.blit(original_screen, (0, 0))
            return ("ok", (rows_value, cols_value, mines_value))
        elif back_button.collidepoint(mouse_pos):
            self.ui.screen.blit(original_screen, (0, 0))
            return ("back", None)
        else:
            return ("update", {"active_slider": None, "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})

    def _handle_mouse_up(self, game_settings):
        """Käsittelee hiiren vapautustapahtumat.

        Args:
            game_settings: Sanakirja, joka sisältää asetukset

        Returns:
            tuple: (action, values)
        """
        rows_value = game_settings['rows_value']
        cols_value = game_settings['cols_value']
        mines_value = game_settings['mines_value']

        return ("update", {"active_slider": None, "rows_value": rows_value,
                          "cols_value": cols_value, "mines_value": mines_value})

    def _handle_mouse_motion(self, event, game_settings, active_slider):
        """Käsittelee hiiren liikutustapahtumat.

        Args:
            event: Pygame-tapahtuma
            game_settings: Sanakirja, joka sisältää asetukset
            active_slider: Aktiivinen liukusäädin

        Returns:
            tuple: (action, values)
        """
        mouse_x = event.pos[0]
        rows_value = game_settings['rows_value']
        cols_value = game_settings['cols_value']
        mines_value = game_settings['mines_value']
        min_size = game_settings['min_size']
        max_size = game_settings['max_size']
        max_mines = game_settings['max_mines']
        rows_slider = game_settings['rows_slider']
        cols_slider = game_settings['cols_slider']
        mines_slider = game_settings['mines_slider']
        slider_width = game_settings['slider_width']

        if active_slider == "rows":
            new_rows_value = self._calculate_slider_value(mouse_x, rows_slider.left,
                                                         slider_width, min_size, max_size)
            return ("update", {"active_slider": active_slider, "rows_value": new_rows_value,
                              "cols_value": cols_value, "mines_value": mines_value})
        elif active_slider == "cols":
            new_cols_value = self._calculate_slider_value(mouse_x, cols_slider.left,
                                                         slider_width, min_size, max_size)
            return ("update", {"active_slider": active_slider, "rows_value": rows_value,
                              "cols_value": new_cols_value, "mines_value": mines_value})
        elif active_slider == "mines":
            new_mines_value = int((mouse_x - mines_slider.left) / slider_width * max_mines)
            new_mines_value = max(1, min(max_mines, new_mines_value))
            return ("update", {"active_slider": active_slider, "rows_value": rows_value,
                              "cols_value": cols_value, "mines_value": new_mines_value})

    def _calculate_slider_value(self, mouse_x, slider_left, slider_width, min_value, max_value):
        """Laskee liukusäätimen arvon hiiren sijainnin perusteella.

        Args:
            mouse_x: Hiiren x-koordinaatti
            slider_left: Liukusäätimen vasemman reunan x-koordinaatti
            slider_width: Liukusäätimen leveys
            min_value: Liukusäätimen minimiarvo
            max_value: Liukusäätimen maksimiarvo

        Returns:
            int: Liukusäätimen arvo
        """
        value = min_value + (mouse_x - slider_left) / slider_width * (max_value - min_value)
        return max(min_value, min(max_value, int(value)))
    #Generoitu koodi loppuu