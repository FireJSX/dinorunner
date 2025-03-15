import pygame
import os


class SpriteSheet:
    """
    Eine Klasse zur Verarbeitung von Sprite-Sheets und Extraktion einzelner Frames.

    Attributes:
        spritesheet (pygame.Surface or None): Das geladene Sprite-Sheet-Bild.
        frame_width (int): Die Breite eines einzelnen Frames.
        frame_height (int): Die Höhe eines einzelnen Frames.
        frames (list): Eine Liste der extrahierten Frames als Pygame-Surfaces.
    """
    def __init__(self, filename, frame_width, frame_height):
        """
        Initialisiert ein SpriteSheet-Objekt, lädt das Bild und extrahiert die Frames.

        Args:
            filename (str): Der Pfad zur Sprite-Sheet-Datei.
            frame_width (int): Die Breite jedes einzelnen Frames.
            frame_height (int): Die Höhe jedes einzelnen Frames.
        """
        if os.path.exists(filename):
            self.spritesheet = pygame.image.load(filename).convert_alpha()
            self.frame_width = frame_width
            self.frame_height = frame_height
            self.frames = self._extract_frames()
        else:
            self.spritesheet = None
            self.frames = []

    def _extract_frames(self):
        """
        Extrahiert einzelne Frames aus dem Sprite-Sheet basierend auf der angegebenen Frame-Größe.

        Returns:
            list: Eine Liste von Pygame-Surfaces, die die extrahierten Frames enthalten.
        """
        sheet_width, sheet_height = self.spritesheet.get_size()
        frames = []

        # Debug: Zeige die Abmessungen des Spritesheets
        print(f"SpriteSheet Größe: {sheet_width}x{sheet_height}")
        print(f"Frame Größe: {self.frame_width}x{self.frame_height}")

        # Überprüfe, wie viele Frames wir in X und Y Richtung extrahieren können
        for y in range(0, sheet_height, self.frame_height):
            for x in range(0, sheet_width, self.frame_width):
                # Wenn das Rechteck noch innerhalb des Spritesheets liegt
                if x + self.frame_width <= sheet_width and y + self.frame_height <= sheet_height:
                    frame = self.spritesheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                    frames.append(frame)
                    # Debug: Ausgabe von jedem extrahierten Frame
                    print(f"Frame extrahiert: {x}, {y} - Größe: {self.frame_width}x{self.frame_height}")

        # Debug: Ausgabe der Anzahl der extrahierten Frames
        print(f"Anzahl extrahierter Frames: {len(frames)}")

        return frames

    def get_frame(self, index):
        """
        Gibt einen bestimmten Frame aus dem Sprite-Sheet zurück.

        Args:
            index (int): Der Index des gewünschten Frames.

        Returns:
            pygame.Surface or None: Das extrahierte Frame-Bild oder None, falls keine Frames vorhanden sind.
        """
        if self.frames:
            return self.frames[index % len(self.frames)]
        return None
