# main_menu.py
import pygame
import sys
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='game_log.log',
    filemode='a'
)

# Init Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu - Space Invaders Pro")

# Warna dan Font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
font_title = pygame.font.Font(None, 72)
font_option = pygame.font.Font(None, 36)

def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def show_settings():
    volume = pygame.mixer.music.get_volume()
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("SETTINGS", font_title, GREEN, WIDTH // 2, HEIGHT // 6)
        draw_text("Controls:", font_option, WHITE, WIDTH // 2, HEIGHT // 4)
        draw_text("Move    : Left/Right", font_option, WHITE, WIDTH // 2, HEIGHT // 4 + 40)
        draw_text("SPACE   : Shoot", font_option, WHITE, WIDTH // 2, HEIGHT // 4 + 80)
        draw_text(" R      : Restart after game over", font_option, WHITE, WIDTH // 2, HEIGHT // 4 + 120)
        draw_text(" M      : Return to main menu after game over", font_option, WHITE, WIDTH // 2, HEIGHT // 4 + 160)
        draw_text(f"Music Volume: {int(volume * 100)}%", font_option, BLUE, WIDTH // 2, HEIGHT // 4 + 220)
        draw_text("Tombol Atas / Tombol Bawah : Adjust volume", font_option, WHITE, WIDTH // 2, HEIGHT // 4 + 260)
        draw_text("Press ESC to return", font_option, WHITE, WIDTH // 2, HEIGHT - 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    volume = min(volume + 0.1, 1.0)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_DOWN:
                    volume = max(volume - 0.1, 0.0)
                    pygame.mixer.music.set_volume(volume)

def show_high_score(high_score):
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("HIGH SCORE", font_title, GREEN, WIDTH // 2, HEIGHT // 4)
        draw_text(f"Top Score: {high_score}", font_option, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press ESC to return", font_option, WHITE, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def main_menu(high_score):
    options = ["Start Game", "Settings", "High Score", "Quit"]
    selected = 0
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("SPACE INVADERS PRO", font_title, GREEN, WIDTH // 2, HEIGHT // 4)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(option, font_option, color, WIDTH // 2, HEIGHT // 2 + i * 40)

        draw_text("Use UP/DOWN to navigate, ENTER to select", font_option, WHITE, WIDTH // 2, HEIGHT - 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected]
                    if choice == "Start Game":
                        return "play"
                    elif choice == "Settings":
                        show_settings()
                    elif choice == "High Score":
                        show_high_score(high_score)
                    elif choice == "Quit":
                        return "quit"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"


    running = True
    while running:
        screen.fill(BLACK)
        draw_text("SPACE INVADERS PRO", font_title, GREEN, WIDTH // 2, HEIGHT // 4)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(option, font_option, color, WIDTH // 2, HEIGHT // 2 + i * 40)

        draw_text("ESC = Exit Game", font_option, RED, WIDTH // 2, HEIGHT // 2 + len(options) * 40 + 20)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game exited from main menu")
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Start Game":
                        logging.info("Starting game from main menu")
                        return  # This lets game.py start the game
                    elif options[selected] == "Settings":
                        logging.info("Opened settings menu")
                        show_settings()
                    elif options[selected] == "High Score":
                        logging.info("Opened high score menu")
                        show_high_score(high_score)
                elif event.key == pygame.K_ESCAPE:
                    logging.info("Game exited by ESC key")
                    pygame.quit(); sys.exit()
if __name__ == "__main__":
    # Ini hanya tampil jika orang iseng menjalankan main_menu.py langsung
    pygame.init()
    warning_screen = pygame.display.set_mode((800, 350))  # Gunakan nama berbeda, jangan 'screen'
    pygame.display.set_caption("Warning!")

    font_large = pygame.font.Font(None, 48)
    font_normal = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)

    running = True
    while running:
        warning_screen.fill((0, 0, 0))

        texts = [
            ("JALANKAN game.py, BUKAN main_menu.py!", font_large, (255, 0, 0)),
            ("THIS GAME MADE BY FARI NOVERI", font_normal, (255, 255, 0)),
            ("Tutup window ini dan:", font_normal, (255, 255, 255)),
            ("1. Buka terminal", font_normal, (255, 255, 255)),
            ("2. Ketik: python game.py", font_normal, (0, 255, 0)),
            ("3. Tekan Enter", font_normal, (255, 255, 255)),
            ("Tekan ESC atau klik X untuk keluar", font_small, (200, 200, 200)),
        ]

        y_pos = 30
        for text, font, color in texts:
            surface = font.render(text, True, color)
            x_pos = (800 - surface.get_width()) // 2
            warning_screen.blit(surface, (x_pos, y_pos))
            y_pos += 45

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()
