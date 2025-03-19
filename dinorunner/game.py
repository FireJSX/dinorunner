import pygame
import asyncio
from .logic import Player, ObstacleManager, load_highscore, save_highscore
from .gui import UI, GameController, BackgroundImage, Floor
from .sfx import sound_manager

pygame.init()
pygame.font.init()

# Game constants
WHITE = (255, 255, 255); BLACK = (0, 0, 0); GREEN = (0, 255, 0); BLUE = (0, 0, 255); RED = (255, 0, 0)

# Game variables
score = 0
highscore_value = 0
player_size = 20
gravity = 1
speed = 5
obstacle_speed = 2
active = False
last_speed_increase = -10  # Speichert die letzte 10er-Marke

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

fps = 60
font = pygame.font.SysFont("helvetica", 16)
timer = pygame.time.Clock()

sound_manager.load_music()
sound_manager.standard_volume()
sound_manager.load_jump_sound()
sound_manager.load_death_sound()
ui = UI(screen_width, screen_height)
game_controller = GameController(screen)

player = Player(50, screen_width - 100 - player_size, player_size, speed, gravity, ui)
obstacles = ObstacleManager(screen_width, player_size // 2, obstacle_speed, ui)
background = BackgroundImage(ui.get_ressources_path("graphics/moon_background.png"), screen_width, screen_height, ui.get_ressources_path)
floor = Floor(screen, ui.get_ressources_path("graphics/floor.png"), ui.get_ressources_path)

# Der Hauptteil des Spiels startet hier
import asyncio

async def main():
    """
    Hauptspiel-Schleife
    """
    global score, highscore_value, active, last_speed_increase, player, obstacles, speed

    running = True

    while running:
        timer.tick(fps)
        y_change = 0
        highscore_value = load_highscore(ui)
        background.blit(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (screen_width - score_text.get_width() - 25, 20))
        highscore_text = font.render(f"Highscore: {highscore_value}", True, WHITE)
        screen.blit(highscore_text, (20, 20))

        player.update_animation()
        floor.update()

        if active:
            sound_manager.play_background_music()
            obstacles.draw(screen)

        if not active:
            ui.start_screen(screen, screen_width, screen_height, font)
        else:
            keys = pygame.key.get_pressed()
            player.move(keys, screen_height - 100, screen_width - player_size * 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("Exit game")
            y_change = game_controller.handle_input(event, y_change)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ui.pause_menu()
                if event.key == pygame.K_SPACE and not active:
                    player = Player(50, screen_height - 100 - player_size, player_size, speed, gravity, ui)
                    obstacles = ObstacleManager(screen_width, player_size, obstacle_speed, ui)
                    score = 0
                    active = True

        if active:
            score += obstacles.move_obstacles(active)

            if obstacles.check_collision(player.get_rect()):
                sound_manager.play_death_sound()
                if score > highscore_value:
                    highscore_value = score
                    save_highscore(highscore_value, ui)
                active = False

            # Geschwindigkeit NUR alle 10 Punkte erhöhen
            if score >= last_speed_increase + 10:
                obstacles.speed += 0.5  # Langsame Erhöhung
                last_speed_increase = score  # Merkt sich, wann zuletzt erhöht wurde

        screen.blit(player.image, (player.x, player.y - player_size))
        ui.manager.draw_ui(screen)

        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()

# Dieser Block sorgt dafür, dass das Skript nur dann ausgeführt wird, wenn es direkt gestartet wird
if __name__ == "__main__":
    main()