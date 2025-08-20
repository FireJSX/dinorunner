import pygame
import pygame_gui
import sys
import os
from .sfx import sound_manager

class UI:
    """
    Die Hauptklasse für die Benutzeroberfläche des Spiels.
    """
    screen_width = 800
    screen_height = 600

    def __init__(self, screen_width, screen_height):
        pygame.init()
        pygame.font.init()

        # tatsächliche Größe speichern (nicht nur die Klassen-Defaults)
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.fullscreen = False
        self.font = pygame.font.SysFont('helvetica', 35, True, False)

        # Theme laden (global für ALLE Buttons)
        theme_path = self.get_ressources_path('ui/theme.json')

        # <<< temporär ins Theme-Verzeichnis wechseln, damit relative Pfade wie "img/..." sicher gefunden werden
        if os.path.exists(theme_path):
            original_cwd = os.getcwd()
            theme_dir = os.path.dirname(theme_path)
            try:
                os.chdir(theme_dir)
                self.manager = pygame_gui.UIManager((screen_width, screen_height), theme_path=theme_path)
            finally:
                os.chdir(original_cwd)
        else:
            self.manager = pygame_gui.UIManager((screen_width, screen_height))
        # >>>

        # --- Debug: prüfen, ob Theme und Images wirklich erreichbar sind ---
        print("Theme geladen:", os.path.exists(theme_path), theme_path)
        theme_dir = os.path.dirname(theme_path)

        # Variante B: images unter ressources/ui/img/
        img_b_normal = os.path.join(theme_dir, "img", "button_normal.png")
        img_b_hover  = os.path.join(theme_dir, "img", "button_hover.png")
        img_b_press  = os.path.join(theme_dir, "img", "button_pressed.png")

        # Variante A: images unter ressources/graphics/ui/ (eine Ebene höher)
        img_a_normal = os.path.join(theme_dir, "..", "graphics", "ui", "button_normal.png")
        img_a_hover  = os.path.join(theme_dir, "..", "graphics", "ui", "button_hover.png")
        img_a_press  = os.path.join(theme_dir, "..", "graphics", "ui", "button_pressed.png")

        print("[B] Normal-Image exists:", os.path.exists(img_b_normal), "->", img_b_normal)
        print("[B] Hover-Image  exists:", os.path.exists(img_b_hover),  "->", img_b_hover)
        print("[B] Press-Image  exists:", os.path.exists(img_b_press),  "->", img_b_press)

        print("[A] Normal-Image exists:", os.path.exists(img_a_normal), "->", os.path.abspath(img_a_normal))
        print("[A] Hover-Image  exists:", os.path.exists(img_a_hover),  "->", os.path.abspath(img_a_hover))
        print("[A] Press-Image  exists:", os.path.exists(img_a_press),  "->", os.path.abspath(img_a_press))
        # ------------------------------------------------------------------

        self.FPS = 60
        self.volume = 0.5
        self.volume_slider = None
        self.clock = pygame.time.Clock()
        self.pause_menu_active = False
        self.main_menu_elements = []
        self.pause_menu_elements = []
        self.sound_manager = sound_manager

    def get_ressources_path(self, filename):
        """
        Pfad, der sowohl im Dev-Modus als auch in einer PyInstaller-EXE funktioniert.
        Achtung: 'ressources' liegt eine Ebene über diesem Modul.
        """
        base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        return os.path.join(base, 'ressources', filename)

    def start_screen(self, screen, screen_width, screen_height, font):
        WHITE = (255, 255, 255)
        font.set_point_size(32)
        font.set_bold(True)
        default_text = font.render("Press SPACE to start", True, (WHITE))
        screen.blit(default_text, (screen_width // 2 - default_text.get_width() // 2, screen_height // 2 - 100))
        default_text2 = font.render("Press SPACE to jump and A/D to move", True, WHITE)
        screen.blit(default_text2, (screen_width // 2 - default_text2.get_width() // 2,
                                    screen_height // 2 - default_text2.get_height() // 2 + default_text.get_height() - 80))
        font.set_point_size(16)
        font.set_bold(False)
        copyright = font.render("© 2025 Jonas 'FireJSX' Vogel", True, WHITE)
        screen.blit(copyright, (screen_width // 2 - copyright.get_width() // 2,
                                screen_height - copyright.get_height() - 20))
        font.set_bold(False)

    def pause_menu(self):
        self.pause_menu_active = True
        paused = True

        # Lade den Hintergrund und das Overlay für das Pause-Menü
        pause_background = pygame.image.load(self.get_ressources_path('graphics/background.jpg')).convert_alpha()
        pause_background.set_alpha(250)

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        original_width, original_height = pause_background.get_size()
        scale_factor_x = screen_width / original_width
        scale_factor_y = screen_height / original_height
        scale_factor = max(scale_factor_x, scale_factor_y)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        x_position = int((new_width - screen_width) / 2) * -1
        y_position = int((new_height - screen_height) / 2) * -1
        scaled_pause_background = pygame.transform.scale(pause_background, (new_width, new_height))

        # Transparentes Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))  # Schwarze Füllung
        overlay.set_alpha(120)  # Transparenzwert

        # Buttons für das Pause-Menü
        button_width = 200
        button_height = 50
        spacing = 20
        center_x = screen_width // 2 - button_width // 2
        start_y = screen_height // 2 - (button_height + spacing)

        # Keine object_id -> Theme gilt GLOBAL
        resume_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y), (button_width, button_height)),
            text='Continue',
            manager=self.manager
        )

        main_menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + button_height + spacing), (button_width, button_height)),
            text='Main Menu',
            manager=self.manager
        )

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + 2 * (button_height + spacing)),
                                      (button_width, button_height)),
            text='Exit game',
            manager=self.manager
        )

        self.pause_menu_elements = [resume_button, main_menu_button, quit_button]

        # Musikpause und Lautstärkeregelung
        sound_manager.set_volume(0.1)  # Lautstärke verringern

        while paused:
            time_delta = self.clock.tick(self.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    paused = False  # Pausieren abbrechen

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == resume_button:
                            paused = False
                            sound_manager.set_volume(0.5)  # Lautstärke zurücksetzen
                            sound_manager.resume_music()  # Musik fortsetzen
                        elif event.ui_element == main_menu_button:
                            self._clear_pause_menu_elements()
                            self.pause_menu_active = False
                            sound_manager.stop_music()  # Ingame-Musik stoppen
                            sound_manager.play_music("nguu.ogg", volume=0.5)  # Hauptmenü-Musik abspielen
                            self.show_main_menu()  # Zum Hauptmenü wechseln
                            return
                        elif event.ui_element == quit_button:
                            pygame.quit()
                            sys.exit()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            # Hintergrund und Overlay anzeigen
            self.screen.blit(scaled_pause_background, (x_position, y_position))
            self.screen.blit(overlay, (0, 0))

            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        # Menü verlassen
        sound_manager.set_volume(0.5)
        for element in self.pause_menu_elements:
            element.kill()
        self.pause_menu_elements.clear()
        self.pause_menu_active = False

        # UIManager nach dem Menü neu mit Theme initialisieren
        theme_path = self.get_ressources_path('ui/theme.json')

        # <<< auch hier kurz ins Theme-Verzeichnis wechseln
        if os.path.exists(theme_path):
            original_cwd = os.getcwd()
            theme_dir = os.path.dirname(theme_path)
            try:
                os.chdir(theme_dir)
                self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height), theme_path=theme_path)
            finally:
                os.chdir(original_cwd)
        else:
            self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        # >>>

    def _clear_pause_menu_elements(self):
        for element in self.pause_menu_elements:
            element.kill()
        self.pause_menu_elements.clear()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu()
            self.manager.process_events(event)

        time_delta = self.clock.tick(self.FPS) / 1000
        self.manager.update(time_delta)
        self.screen.fill((0, 0, 0))
        if not self.pause_menu_active:
            self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def show_main_menu(self):
        self.main_menu_active = True

        try:
            background = pygame.image.load(self.get_ressources_path('graphics/MainMenu.png')).convert()
            background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        except:
            background = None

        button_width = 200
        button_height = 50
        spacing = 20
        center_x = self.screen.get_width() // 2 - button_width // 2
        start_y = self.screen.get_height() // 2 - (button_height + spacing)

        # Buttons ohne object_id -> verwenden globale Theme-Regel "button"
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y), (button_width, button_height)),
            text='Start game',
            manager=self.manager
        )

        quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((center_x, start_y + button_height + spacing), (button_width, button_height)),
            text='Exit game',
            manager=self.manager
        )

        self.main_menu_elements.extend([start_button, quit_button])

        while self.main_menu_active:
            time_delta = self.clock.tick(self.FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element.text == 'Start game':
                            self.main_menu_active = False
                            for element in self.main_menu_elements:
                                element.kill()
                            self.main_menu_elements.clear()

                        elif event.ui_element.text == 'Exit game':
                            pygame.quit()
                            sys.exit()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            if background:
                self.screen.blit(background, (0, 0))
            else:
                self.screen.fill((30, 30, 30))

            self.manager.draw_ui(self.screen)
            pygame.display.update()

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

    def handle_input(self, event, y_change):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                self.toggle_fullscreen()
            if event.key == pygame.K_F12:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and y_change == 0:
                y_change = 18
        return y_change

    def toggle_fullscreen(self):
        fullscreen = not pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
        if fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

class BackgroundImage:
    def __init__(self, filename, screen_width, screen_height, get_asset_path):
        self.image = pygame.image.load(get_asset_path(filename)).convert_alpha()
        self.original_width, self.original_height = self.image.get_size()
        self.scale_factor_x = screen_width / self.original_width
        self.scale_factor_y = screen_height / self.original_height
        self.scale_factor = max(self.scale_factor_x, self.scale_factor_y)
        self.new_width = int(self.original_width * self.scale_factor)
        self.new_height = int(self.original_height * self.scale_factor)
        self.x_position = int((self.new_width - screen_width) / 2) * -1
        self.y_position = int((self.new_height - screen_height) / 2) * -1
        self.scaled_image = pygame.transform.scale(self.image, (self.new_width, self.new_height))

    def blit(self, screen):
        screen.blit(self.scaled_image, (self.x_position, self.y_position))

class Floor:
    def __init__(self, screen, image_path, get_asset_path):
        self.screen = screen
        self.image = pygame.image.load(get_asset_path(image_path)).convert_alpha()
        self.original_width, self.original_height = self.image.get_size()
        self.screen_width, self.screen_height = screen.get_size()
        new_height = self.original_height * 0.69
        scale_factor = new_height / self.original_height
        new_width = int(self.original_width * scale_factor)
        self.image = pygame.transform.scale(self.image, (new_width, int(new_height)))
        self.rect = self.image.get_rect(bottomleft=(0, self.screen_height))

    def update(self):
        self.screen.blit(self.image, self.rect)
