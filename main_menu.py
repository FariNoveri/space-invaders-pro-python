import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Main Menu - Space Invaders Pro")

# Warna dan Font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)
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
    running = True
    while running:
        screen.fill(BLACK)
        draw_text("SETTINGS", font_title, GREEN, WIDTH // 2, HEIGHT // 4)
        draw_text("Press ESC to return", font_option, WHITE, WIDTH // 2, HEIGHT // 2)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def show_high_score():
    running = True
    # High score bisa diambil dari file nanti, ini hanya dummy
    high_score = 1230
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

def main_menu():
    options = ["Start Game", "Settings", "High Score"]
    selected = 0

    while True:
        screen.fill(BLACK)
        draw_text("SPACE INVADERS PRO", font_title, GREEN, WIDTH // 2, HEIGHT // 4)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(option, font_option, color, WIDTH // 2, HEIGHT // 2 + i * 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Start Game":
                        return  # Mulai game
                    elif options[selected] == "Settings":
                        show_settings()
                    elif options[selected] == "High Score":
                        show_high_score()
