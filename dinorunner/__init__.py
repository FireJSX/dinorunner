
# Importiere wichtige Klassen und Funktionen aus den Modulen
from .logic import Player, ObstacleManager, load_highscore, save_highscore
from .gui import UI, GameController
from .sfx import sound_manager
from .gfx import SpriteSheet

# (Optional) Du kannst auch Versionen oder Metadaten hinzufügen, falls benötigt
__version__ = "0.0.1"
__title__ = "dinorunner"