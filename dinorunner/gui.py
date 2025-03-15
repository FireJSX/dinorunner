import pygame
import pygame_gui
import sys
import os

class UI:
    """
    Die Hauptklasse für die Benutzeroberfläche des Spiels.

    Attributes:
        screen (pygame.Surface): Das Hauptanzeigefenster.
        fullscreen (bool): Gibt an, ob das Spiel im Vollbildmodus ist.
        font (pygame.font.Font): Schriftart für Texte.
        manager (pygame_gui.UIManager): Verwalter für UI-Elemente.
        FPS (int): Die Anzahl der Frames pro Sekunde.
        volume (float): Die Lautstärke des Spiels.
        volume_slider (None): Platzhalter für einen Lautstärkeregler.
        clock (pygame.time.Clock): Pygame-Uhr für Framerate-Kontrolle.
        pause_menu_active (bool): Gibt an, ob das Pausenmenü aktiv ist.
    """
    screen_width = 800
    screen_height = 600

    def __init__(self, screen_width, screen_height):
        """
        Initialisiert die Benutzeroberfläche und setzt alle UI-Elemente.

        Args:
            screen_width (int): Die Breite des Spielfensters.
            screen_height (int): Die Höhe des Spielfensters.
        """
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.fullscreen = False
        self.font = pygame.font.SysFont('helvetica', 35, True, False)
        self.manager = pygame_gui.UIManager((screen_width, screen_height))
        self.FPS = 60
        self.volume = 0.5
        self.volume_slider = None
        self.clock = pygame.time.Clock()
        self.pause_menu_active = False

    def get_ressources_path(self, filename):
        """
        Gibt den absoluten Pfad einer Datei zurück, relativ zum aktuellen Skriptverzeichnis.

        Args:
            filename (str): Der Dateiname.

        Returns:
            str: Der absolute Pfad zur Datei.
        """
        return os.path.join(os.path.dirname(__file__), '..', 'ressources', filename)

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
        """
        Zeigt das Pausenmenü an und hält das Spiel an, bis der Benutzer es verlässt.
        """
        self.pause_menu_active = True
        paused = True

        # Verwende die get_asset_path-Methode, um den Pfad zu den Bildern zu erhalten
        exit_button_image = pygame.image.load(self.get_ressources_path(
            'graphics/exit-button-md.png')).convert_alpha()
        exit_button_rect = exit_button_image.get_rect(topleft=(15, 10))
        exit_button_image = pygame.transform.scale(exit_button_image, (exit_button_image.get_width() // 2, exit_button_image.get_height() // 2))

        pause_background = pygame.image.load(self.get_ressources_path(
            'graphics/background.jpg')).convert_alpha()

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

        while paused:
            self.screen.blit(scaled_pause_background, (x_position, y_position))
            pause_text = self.font.render("Game paused – Press 'ESC' to continue", True, (255, 255, 255))
            text_rect = pause_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))

            self.screen.blit(exit_button_image, exit_button_rect)
            self.screen.blit(pause_text, text_rect)
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if exit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

            time_delta = self.clock.tick(self.FPS) / 1000
            self.manager.update(time_delta)
            self.screen.fill((0, 0, 0))
            self.manager.draw_ui(self.screen)
        self.pause_menu_active = False

    def update(self):
        """
        Aktualisiert das UI, verarbeitet Benutzereingaben und rendert das Interface.
        """
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

# Diese Klassen sollten außerhalb von UI stehen:
class GameController:
    """
    Verwaltet die Spielereingaben und das Spielfenster.

    Attributes:
        screen (pygame.Surface): Die Hauptanzeige des Spiels.
        screen_width (int): Breite des Spielfensters.
        screen_height (int): Höhe des Spielfensters.
    """
    def __init__(self, screen):
        """
        Initialisiert den Game-Controller.

        Args:
            screen (pygame.Surface): Die Hauptanzeige des Spiels.
        """
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

    def handle_input(self, event, y_change):
        """
        Behandelt die Eingaben des Spielers.

        Args:
            event (pygame.event.Event): Das aktuelle Eingabeereignis.
            y_change (int): Die vertikale Bewegung des Spielers.

        Returns:
            int: Die aktualisierte vertikale Bewegung des Spielers.
        """
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
        """
        Schaltet zwischen Vollbild- und Fenstermodus um.
        """
        fullscreen = not pygame.display.get_surface().get_flags() & pygame.FULLSCREEN
        if fullscreen:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

class BackgroundImage:
    """
    Klasse zur Verwaltung und Skalierung des Hintergrundbildes.

    Attributes:
        image (pygame.Surface): Das geladene Bild des Hintergrunds.
        scaled_image (pygame.Surface): Die skalierte Version des Hintergrundbildes.
        x_position (int): X-Position des Bildes.
        y_position (int): Y-Position des Bildes.
    """
    def __init__(self, filename, screen_width, screen_height, get_asset_path):
        """
        Initialisiert das Hintergrundbild.

        Args:
            screen (pygame.Surface): Das Hauptfenster des Spiels.
            filename (str): Der Dateiname des Bildes.
            get_asset_path (function): Funktion zur Ermittlung des vollständigen Dateipfads.
        """
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
        """
        Zeichnet den Hintergrund auf den Bildschirm.
        """
        screen.blit(self.scaled_image, (self.x_position, self.y_position))

class Floor:
    """
    Klasse für das Bodenbild im Spiel.

    Attributes:
        screen (pygame.Surface): Das Spielfenster.
        image (pygame.Surface): Das Bild des Bodens.
        rect (pygame.Rect): Das Rechteck für die Position des Bodens.
    """
    def __init__(self, screen, image_path, get_asset_path):
        """
        Initialisiert den Boden mit einem Bild.

        Args:
            screen (pygame.Surface): Das Hauptfenster des Spiels.
            image_path (str): Der Pfad zum Bild des Bodens.
            get_asset_path (function): Funktion zur Bestimmung des Bildpfads.
        """
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
        """
        Zeichnet das Bodenbild auf das Spielfenster.
        """
        self.screen.blit(self.image, self.rect)