import os
import pygame

class SoundManager:
    """
    Verwaltet die Soundeffekte und Hintergrundmusik des Spiels.

    Attributes:
        volume (float): Standardlautstärke der Hintergrundmusik.
        sound_dir (str): Verzeichnis für die Sounddateien.
        background_music_file (str): Pfad zur Hintergrundmusikdatei.
        jump_sound_file (str): Pfad zur Sprung-Sounddatei.
        death_sound_file (str): Pfad zur Todes-Sounddatei.
        jump_sound_volume (float): Lautstärke des Sprung-Sounds.
        jump_sound (pygame.mixer.Sound): Geladener Sprung-Sound.
        death_sound (pygame.mixer.Sound): Geladener Todes-Sound.
    """
    def __init__(self):
        """
        Initialisiert den SoundManager und lädt die Sounddateien.
        """
        pygame.init()
        pygame.mixer.init()
        self.volume = 0.5

        # Verzeichnis des aktuellen Scripts
        self.sound_dir = os.path.join(os.path.dirname(__file__), ".\\ressources\\sound")

        # Sounddateien mit absolutem Pfad referenzieren
        self.background_music_file = os.path.join(self.sound_dir, "somebody_told_you.ogg")
        self.jump_sound_file = os.path.join(self.sound_dir, "jump-sound.ogg")
        self.death_sound_file = os.path.join(self.sound_dir, "death-sound.ogg")

        self.jump_sound_volume = 0.2
        self.jump_sound = None
        self.death_sound = None

    def standard_volume(self):
        """
        Setzt die Lautstärke der Hintergrundmusik auf den Standardwert.
        """
        pygame.mixer.music.set_volume(self.volume)

    def load_music(self):
        """
        Lädt die Hintergrundmusik, falls die Datei existiert.
        """
        try:
            if not os.path.exists(self.background_music_file):
                raise FileNotFoundError(f"Musikdatei nicht gefunden: {self.background_music_file}")
            pygame.mixer.music.load(self.background_music_file)
            print("Musik geladen:", self.background_music_file)
        except Exception as e:
            print("Fehler beim Laden der Musik:", e)

    def play_background_music(self):
        """
        Startet die Hintergrundmusik in einer Endlosschleife.
        """
        if self.background_music_file and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1, 0.0)
            print("Hintergrundmusik spielt.")

    def load_jump_sound(self):
        """
        Lädt den Sprung-Sound aus der Datei.
        """
        if not os.path.exists(self.jump_sound_file):
            raise FileNotFoundError(f"Jump-Sound nicht gefunden: {self.jump_sound_file}")
        self.jump_sound = pygame.mixer.Sound(self.jump_sound_file)

    def play_jump_sound(self):
        """
        Spielt den geladenen Sprung-Sound ab.
        """
        if self.jump_sound:
            self.jump_sound.set_volume(self.jump_sound_volume)
            self.jump_sound.play()

    def load_death_sound(self):
        """
        Lädt den Todes-Sound aus der Datei.
        """
        if not os.path.exists(self.death_sound_file):
            raise FileNotFoundError(f"Death-Sound nicht gefunden: {self.death_sound_file}")
        self.death_sound = pygame.mixer.Sound(self.death_sound_file)

    def play_death_sound(self):
        """
        Spielt den geladenen Todes-Sound ab.
        """
        if self.death_sound:
            self.death_sound.play()

# Instanz erstellen
sound_manager = SoundManager()