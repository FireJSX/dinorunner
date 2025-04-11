import pygame
import asyncio
from .logic import Player, ObstacleManager, load_highscore, save_highscore
from .gui import UI, GameController, BackgroundImage, Floor
from .sfx import sound_manager

pygame.init()
pygame.font.init()

# Game constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game variables
score = 0
highscore_value = 0
player_size = 20
gravity = 1
speed = 5
obstacle_speed = 2
active = False
last_speed_increase = -10

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

fps = 60
font = pygame.font.SysFont("helvetica", 16)
timer = pygame.time.Clock()

sound_manager.load_jump_sound()
sound_manager.load_death_sound()
ui = UI(screen_width, screen_height)
game_controller = GameController(screen)

player = Player(50, screen_width - 100 - player_size, player_size, speed, gravity, ui)
obstacles = ObstacleManager(screen_width, player_size // 2, obstacle_speed, ui)
background = BackgroundImage(ui.get_ressources_path("graphics/moon_background.png"), screen_width, screen_height,
                             ui.get_ressources_path)
floor = Floor(screen, ui.get_ressources_path("graphics/floor.png"), ui.get_ressources_path)


# Hauptspiel-Schleife
async def main():
    global score, highscore_value, active, last_speed_increase, player, obstacles, speed

    # Musik im Hauptmenü starten (nguu.ogg)
    sound_manager.play_music("nguu.ogg", volume=0.5)

    ui.show_main_menu(game_controller)  # Hauptmenü anzeigen
    pygame.time.delay(1000)  # Eventuell eine kleine Pause für den Start

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
            sound_manager.play_background_music()  # Ingame-Musik abspielen
            obstacles.draw(screen)

        if not active:
            ui.start_screen(screen, screen_width, screen_height, font)
        else:
            keys = pygame.key.get_pressed()
            player.move(keys, screen_height - 100, screen_width - player_size * 2)

        for event in pygame.event.get():
            game_controller.handle_input(event)
            if event.type == pygame.QUIT:
                running = False
                print("Exit game")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if active:
                        # Ins Pause-Menü wechseln
                        print("Escape gedrückt, Spiel pausieren")  # Debugging
                        sound_manager.set_volume(0.1)  # Lautstärke reduzieren, aber Musik läuft weiter
                        ui.pause_menu(game_controller)  # Pause-Menü anzeigen
                    else:
                        # Ins Hauptmenü zurückkehren
                        print("Escape gedrückt, zurück ins Hauptmenü")  # Debugging
                        sound_manager.play_music("nguu.ogg", volume=0.5)  # Hauptmenü-Musik abspielen
                        sound_manager.set_volume(0.5)  # Lautstärke auf 0.5 zurücksetzen
                        active=False

                if event.key == pygame.K_SPACE and not active:
                    # Spiel starten
                    print("Start game: Neue Musik abspielen")  # Debugging
                    sound_manager.stop_music()  # Zuerst die aktuelle Musik stoppen
                    sound_manager.play_music("somebody_told_you.ogg", volume=0.5)  # Neue Ingame-Musik abspielen
                    sound_manager.set_volume(0.5)  # Lautstärke auf Standard zurücksetzen
                    player = Player(50, screen_height - 100 - player_size, player_size, speed, gravity, ui)
                    obstacles = ObstacleManager(screen_width, player_size, obstacle_speed, ui)
                    score = 0
                    active = True

        if active:
            score += obstacles.move_obstacles(active)

            if obstacles.check_collision(player.get_rect()):
                sound_manager.stop_music()  # Musik stoppen
                sound_manager.play_death_sound()  # Tod-Sound abspielen
                print("Kollision erkannt, stoppe Musik")  # Debugging
                if score > highscore_value:
                    highscore_value = score
                    save_highscore(highscore_value, ui)
                active = False
                # Beim Spielende zurück zur Hauptmusik
                print("Spiel vorbei: Zurück zur Hauptmusik (nguu.ogg)")  # Debugging
                sound_manager.play_music("nguu.ogg", volume=0.5)  # Hauptmusik zurücksetzen
                sound_manager.set_volume(0.5)  # Lautstärke zurück auf Standard

            if score >= last_speed_increase + 10:
                obstacles.speed += 0.5
                last_speed_increase = score

        screen.blit(player.image, (player.x, player.y - player_size))
        ui.manager.draw_ui(screen)

        pygame.display.flip()
        await asyncio.sleep(0)

    pygame.quit()


# Nur ausführen, wenn direkt gestartet
if __name__ == "__main__":
    asyncio.run(main())
