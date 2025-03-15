import pygame
import random
import json
from .sfx import sound_manager
from .gfx import SpriteSheet
from .gui import UI
import os

class Player:
    """
    Diese Klasse repräsentiert einen Spieler im Spiel, der sich bewegen kann und mit Hindernissen interagiert.

    Attributes:
        x (int): Die x-Position des Spielers.
        y (int): Die y-Position des Spielers.
        size (int): Die Größe des Spielers.
        speed (int): Die Geschwindigkeit des Spielers.
        gravity (int): Die Schwerkraft, die auf den Spieler wirkt.
        y_change (int): Die Änderung der y-Position des Spielers (vertikale Bewegung).
        x_change (int): Die Änderung der x-Position des Spielers (horizontale Bewegung).
        on_ground (bool): Gibt an, ob der Spieler den Boden berührt.
        state (str): Der aktuelle Zustand des Spielers (idle, walk, jump).
        image (Surface): Das aktuelle Bild des Spielers (basierend auf der Animation).
        walk_images (list): Liste der Bilder für die Gehen-Animation.
        jump_images (list): Liste der Bilder für die Springen-Animation.
        idle_images (list): Liste der Bilder für die Idle-Animation.
        animation_timer (float): Timer zur Steuerung der Animationsgeschwindigkeit.
        animation_speed (float): Geschwindigkeit, mit der die Animationen wechseln.
        walk_frame_index (int): Der Index des aktuellen Gehen-Frames.
    """
    def __init__(self, x, y, size, speed, gravity, ui, idle_image=None):
        """
                Initialisiert den Spieler mit den angegebenen Werten.

                Args:
                    x (int): Die x-Position des Spielers.
                    y (int): Die y-Position des Spielers.
                    size (int): Die Größe des Spielers.
                    speed (int): Die Geschwindigkeit des Spielers.
                    gravity (int): Die Schwerkraft des Spiels.
                    ui (UI): Das Benutzerinterface für den Zugriff auf Assets.
                    idle_image (Surface, optional): Ein Bild für die Idle-Animation. Standard ist None.
                """
        self.ui = ui
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.gravity = gravity
        self.y_change = 0
        self.x_change = 0
        self.on_ground = False
        self.state = 'idle'  # Initialer Zustand ist 'idle'

        # Standardwerte für Animationen
        self.image = None
        self.walk_images = []
        self.jump_images = []
        self.idle_images = []
        self.animation_timer = 0
        self.animation_speed = 0.2  # Geschwindigkeit der Animation (kann angepasst werden)
        self.walk_frame_index = 0  # Anfangsindex für den Walk-Frame
        self.jump_frame_index = 0
        self.idle_frame_index = 0
        self.facing_right = True

        # Prüfen, ob die Assets existieren
        self.load_assets()

    def load_assets(self):
        """
                Lädt die benötigten Bilddateien für die verschiedenen Zustände des Spielers
                (Idle, Walk, Jump). Wenn die Bilder nicht gefunden werden, wird ein Platzhalter verwendet.

                Sets:
                    idle_images (list): Liste der Idle-Frames.
                    walk_images (list): Liste der Walk-Frames.
                    jump_images (list): Liste der Jump-Frames.
                """
        # Lade die Assets und überprüfe, ob sie existieren
        idle_path = self.ui.get_ressources_path("assets/dino_idle.png")
        walk_path = self.ui.get_ressources_path("assets/dino_walk.png")
        jump_path = self.ui.get_ressources_path("assets/dino_jump.png")

        # Überprüfen, ob die Dateien existieren und sie laden
        if os.path.exists(idle_path):
            sprite_sheet = SpriteSheet(idle_path, 32, 32)
            self.idle_images = [pygame.transform.scale(frame, (self.size*2.5, self.size*2.5)) for frame in sprite_sheet.frames]
            print(f"Idle Image loaded: {idle_path}")
        else:
            print(f"Idle Image not found: {idle_path}")

        if os.path.exists(walk_path):
            sprite_sheet = SpriteSheet(walk_path, 32, 32)
            self.walk_images = [pygame.transform.scale(frame, (self.size*2.5, self.size*2.5)) for frame in sprite_sheet.frames]
            print(f"Walk Images loaded: {walk_path}")
        else:
            print(f"Walk Image not found: {walk_path}")

        if os.path.exists(jump_path):
            sprite_sheet = SpriteSheet(jump_path, 32, 32)
            self.jump_images = [pygame.transform.scale(frame, (self.size*2.5, self.size*2.5)) for frame in sprite_sheet.frames]
            print(f"Jump Image loaded: {jump_path}")
        else:
            print(f"Jump Image not found: {jump_path}")

        # Wenn keine Assets geladen wurden, ersetze das Bild durch ein Platzhalter-Rechteck
        if not self.idle_images:
            self.idle_images = [pygame.Surface((self.size, self.size))]  # Platzhalter für Idle
            self.idle_images[0].fill((0, 255, 0))  # Grün für den Platzhalter
            print("Using placeholder idle image (green rectangle)")

        if not self.jump_images:
            self.jump_images = [pygame.Surface((self.size, self.size))]  # Platzhalter für Jump
            self.jump_images[0].fill((255, 0, 0))  # Rot für den Platzhalter
            print("Using placeholder jump image (red rectangle)")

        if not self.walk_images:
            self.walk_images = [pygame.Surface((self.size, self.size))]  # Platzhalter für Walk
            self.walk_images[0].fill((0, 0, 255))  # Blau für den Platzhalter
            print("Using placeholder walk image (blue rectangle)")

        # Falls alles korrekt geladen wurde, setze das Standardbild auf Idle
        if self.idle_images:
            self.image = self.idle_images[0]  # Standard-Idle-Sprite (Erster Frame)

    def move(self, keys, floor_top, width):
        """
        Bewegt den Spieler basierend auf den Benutzereingaben.

        Args:
            keys (list): Eine Liste der gedrückten Tasten (z.B. pygame.K_a, pygame.K_d).
            floor_top (int): Die Y-Position des Bodens, den der Spieler nicht überschreiten darf.
            width (int): Die Breite des Bildschirms, um Kollision mit dem rechten Rand zu verhindern.
        """
        if keys[pygame.K_a] and self.x>0:
            self.x_change = -self.speed
            self.state = 'walk'  # Wenn sich der Spieler nach links bewegt, wird der Walk-Zustand aktiviert
        elif keys[pygame.K_d] and self.x<=width:
            self.x_change = self.speed
            self.state = 'walk'  # Wenn sich der Spieler nach rechts bewegt, wird der Walk-Zustand aktiviert
        else:
            self.x_change = 0
            if self.on_ground:
                self.state = 'idle'  # Wenn der Spieler still steht, wird der Idle-Zustand aktiviert

        if keys[pygame.K_SPACE] and self.on_ground:
            self.y_change = 18  # Sprungkraft
            sound_manager.play_jump_sound()
            self.on_ground = False
            self.state = 'jump'  # Wenn der Spieler springt, wird der Jump-Zustand aktiviert

        self.x += self.x_change
        self.y -= self.y_change
        self.y_change -= self.gravity

        if self.y >= floor_top - self.size:
            self.y = floor_top - self.size
            self.y_change = 0
            self.on_ground = True

    def get_rect(self):
        """
        Gibt das Rechteck des Spielers zurück, das für Kollisionserkennung verwendet wird.

        Returns:
            pygame.Rect: Das Rechteck des Spielers.
        """
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def update_animation(self):
        # Erhöhe den Animationstimer immer, unabhängig vom Zustand
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0  # Timer zurücksetzen

            # Wähle die richtige Animationsframe basierend auf dem Zustand
            if self.state == 'walk' and self.walk_images:
                self.walk_frame_index = (self.walk_frame_index + 1) % len(self.walk_images)
                new_image = self.walk_images[self.walk_frame_index]

            elif self.state == 'jump' and self.jump_images:
                self.jump_frame_index = (self.jump_frame_index + 1) % len(self.jump_images)
                new_image = self.jump_images[self.jump_frame_index]

            elif self.state == 'idle' and self.idle_images:
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_images)
                new_image = self.idle_images[self.idle_frame_index]

            else:
                new_image = None  # Falls kein Bild da ist

            # Falls keine Animationen geladen sind, setze eine Standardfarbe
            if new_image is None:
                new_image = pygame.Surface((self.size, self.size))
                new_image.fill((255, 255, 255))

            # Skaliere das Bild
            new_image = pygame.transform.scale(new_image, (self.size * 2, self.size * 2))

            # Überprüfe, ob sich die Blickrichtung geändert hat
            if self.x_change > 0:
                self.facing_right = True
            elif self.x_change < 0:
                self.facing_right = False

            # Falls der Charakter nach links schaut, flippe das Bild **nur einmal**
            if not self.facing_right:
                new_image = pygame.transform.flip(new_image, True, False)

            # Setze das finale Bild
            self.image = new_image

    def draw(self, screen):
        """
        Zeichnet den Spieler auf dem Bildschirm.

        Args:
            screen (pygame.Surface): Das Pygame-Oberflächenobjekt, auf dem der Spieler gezeichnet wird.
        """
        screen.blit(self.image, (self.x, self.y-self.size))


class ObstacleManager:
    """
    Verwaltet die Hindernisse im Spiel, einschließlich deren Bewegung und Kollisionserkennung.

    Attributes:
        obstacles (list): Die Positionen der Hindernisse auf der x-Achse.
        obstacle_images (list): Die Bilder der Hindernisse.
        width (int): Die Breite des Bildschirms.
        player_size (int): Die Größe des Spielers, um Hindernisse entsprechend zu skalieren.
        speed (int): Die Geschwindigkeit der Hindernisse.
    """
    def __init__(self, width, player_size, speed, ui):
        """
        Initialisiert den Hindernis-Manager.

        Args:
            width (int): Die Breite des Bildschirms.
            player_size (int): Die Größe des Spielers, die auch die Größe der Hindernisse bestimmt.
            speed (int): Die Geschwindigkeit der Hindernisse.
            ui (UI): Das Benutzerinterface für den Zugriff auf die Hindernis-Bilder.
        """
        self.ui = ui
        self.obstacles = [width - 150, width, width + 150]  # Anfangsposition der Hindernisse
        self.width = width
        self.player_size = player_size
        self.speed = speed
        self.obstacle_images = []  # Liste für Hindernisbilder
        self.load_obstacle_assets()  # Lädt die Hindernisbilder

    def load_obstacle_assets(self):
        """
        Lädt das Hindernisbild und prüft, ob es vorhanden ist.

        Falls das Bild nicht gefunden wird, wird ein Platzhalter-Bild verwendet.
        """
        # Lade die Hindernisbilder
        obstacle_path = self.ui.get_ressources_path("assets/meteor_1.png")  # Pfad zu deinem Hindernisbilder

        if os.path.exists(obstacle_path):
            obstacle_image = pygame.image.load(obstacle_path)
            obstacle_image = pygame.transform.scale(obstacle_image, (self.player_size, self.player_size))
            self.obstacle_images.append(obstacle_image)
            print(f"Obstacle Image loaded: {obstacle_path}")
        else:
            print(f"Obstacle Image not found: {obstacle_path}")
            # Falls das Bild nicht gefunden wird, erstelle ein Platzhalter-Rechteck
            placeholder_image = pygame.Surface((self.player_size, self.player_size))
            placeholder_image.fill((255, 0, 0))  # Rot als Platzhalter
            self.obstacle_images.append(placeholder_image)
            print("Using placeholder obstacle image (red rectangle)")

    def move_obstacles(self, active):
        """
        Bewegt die Hindernisse auf dem Bildschirm und lässt sie respawnen, wenn sie den Bildschirm verlassen.

        Args:
            active (bool): Gibt an, ob die Hindernisse aktiv bewegt werden sollen.

        Returns:
            int: Die Anzahl der Hindernisse, die den Bildschirm verlassen haben (Punkte).
        """
        points = 0  # Zähler für Punkte
        if active:
            for i in range(len(self.obstacles)):
                self.obstacles[i] -= self.speed  # Bewege das Hindernis nach links

                # Wenn das Hindernis den linken Rand verlässt
                if self.obstacles[i] < -self.player_size:
                    self.obstacles[i] = random.randint(self.width + self.player_size, self.width + self.player_size * 3)
                    points += 1  # Erhöhe den Punktestand um 1

        return points  # Punkte zurückgeben

    def check_collision(self, player_rect):
        """
        Überprüft, ob der Spieler mit einem Hindernis kollidiert.

        Args:
            player_rect (pygame.Rect): Das Rechteck des Spielers, das für die Kollisionserkennung verwendet wird.

        Returns:
            bool: True, wenn eine Kollision erkannt wurde, ansonsten False.
        """
        for obs_x in self.obstacles:
            obstacle_rect = pygame.Rect(obs_x, 500 - self.player_size, self.player_size, self.player_size)
            if player_rect.colliderect(obstacle_rect):
                return True
        return False

    def draw(self, screen):
        """
        Zeichnet die Hindernisse auf dem Bildschirm.

        Args:
            screen (pygame.Surface): Das Pygame-Oberflächenobjekt, auf dem die Hindernisse gezeichnet werden.
        """
        for obs_x in self.obstacles:
            obstacle_rect = pygame.Rect(obs_x, 500 - self.player_size, self.player_size, self.player_size)
            # Zeichne das Hindernisbild
            screen.blit(self.obstacle_images[0], obstacle_rect)  # Wir nehmen hier das erste Hindernisbild


### Highscore-Funktionen ###

def load_highscore(ui):
    """
    Lädt den Highscore aus einer JSON-Datei.

    Args:
        ui (UI): Das Benutzerinterface für den Zugriff auf die Highscore-Datei.

    Returns:
        int: Der gespeicherte Highscore-Wert. Wenn keine Datei existiert oder ein Fehler auftritt, wird 0 zurückgegeben.
    """
    try:
        highscore_path = ui.get_ressources_path("highscore.json")
        with open(highscore_path, "r") as file:
            data = json.load(file)
            return data.get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0  # Falls die Datei nicht existiert oder fehlerhaft ist, setze Highscore auf 0.

def save_highscore(highscore_value, ui):
    """
    Speichert den aktuellen Highscore in einer JSON-Datei.

    Args:
        ui (UI): Das Benutzerinterface für den Zugriff auf die Highscore-Datei.
        score (int): Der aktuelle Highscore, der gespeichert werden soll.
    """
    highscore_path = ui.get_ressources_path("highscore.json")
    with open(highscore_path, "w") as file:
        json.dump({"highscore": highscore_value}, file)