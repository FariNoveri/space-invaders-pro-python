from main_menu import main_menu
import pygame
import random

# Initialize pygame before calling main_menu()
pygame.init()
main_menu()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Pro")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

difficulty_timer = 0
difficulty_level = 1

class Player:
    def __init__(self):
        self.img = pygame.Surface((30, 30))
        self.img.fill(GREEN)
        self.rect = self.img.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.speed = 8
        self.cooldown_time = 15
        self.shoot_cooldown = self.cooldown_time
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = self.cooldown_time
            return Bullet(self.rect.centerx, self.rect.top)
        return None
    
    def update(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def draw(self):
        screen.blit(self.img, self.rect)

class Alien:
    def __init__(self, level=1):
        self.img = pygame.Surface((25, 25))
        self.img.fill(RED)
        self.rect = self.img.get_rect(center=(random.randint(50, WIDTH-50), random.randint(-100, -30)))
        self.speed_x = random.choice([-1.5, -1, 1, 1.5]) * (1 + level * 0.05)
        self.speed_y = random.uniform(0.5, 1.2) * (1 + level * 0.03)
        self.shoot_delay = random.randint(80, 180 - level * 5)
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce when hitting screen edges
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed_x *= -1
        
        # Bounce when hitting middle line
        if self.rect.top > HEIGHT // 2:
            self.rect.top = HEIGHT // 2
            self.speed_y *= -1
        
        self.shoot_delay -= 1
        if self.shoot_delay <= 0:
            self.shoot_delay = random.randint(60, 180)
            return Bullet(self.rect.centerx, self.rect.bottom, BLUE, 5)
        return None
    
    def draw(self):
        screen.blit(self.img, self.rect)

class Bullet:
    def __init__(self, x, y, color=WHITE, speed=-7):
        self.img = pygame.Surface((4, 10))
        self.img.fill(color)
        self.rect = self.img.get_rect(center=(x, y))
        self.speed = speed
    
    def update(self):
        self.rect.y += self.speed
        return self.rect.bottom < 0 or self.rect.top > HEIGHT
    
    def draw(self):
        screen.blit(self.img, self.rect)

# Initialize game objects
player = Player()
bullets = []
alien_bullets = []
aliens = []
score = 0
game_over = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def spawn_alien():
    if random.random() < 0.01 + (0.003 * difficulty_level) and len(aliens) < (5 + difficulty_level * 2):
        aliens.append(Alien(difficulty_level))

# Main Game Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    difficulty_timer += 1

    # Increase difficulty every 10 seconds
    if difficulty_timer % (60 * 10) == 0:
        difficulty_level += 1

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                new_bullet = player.shoot()
                if new_bullet:
                    bullets.append(new_bullet)
            
            elif event.key == pygame.K_r and game_over:
                # Reset game
                player = Player()
                bullets = []
                alien_bullets = []
                aliens = []
                score = 0
                game_over = False
                difficulty_level = 1
                difficulty_timer = 0
            
            elif event.key == pygame.K_m and game_over:
                running = False
                main_menu()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        player.update()
        
        # Spawn new aliens
        spawn_alien()
        
        # Update bullets
        for bullet in bullets[:]:
            if bullet.update():
                bullets.remove(bullet)
        
        # Update alien bullets
        for bullet in alien_bullets[:]:
            if bullet.update():
                alien_bullets.remove(bullet)
        
        # Update aliens
        for alien in aliens[:]:
            new_bullet = alien.update()
            if new_bullet:
                alien_bullets.append(new_bullet)
            
            # Check bullet collisions
            for bullet in bullets[:]:
                if alien.rect.colliderect(bullet.rect):
                    aliens.remove(alien)
                    bullets.remove(bullet)
                    score += 10
                    break
        
        # Check player hit by alien bullet
        for bullet in alien_bullets[:]:
            if player.rect.colliderect(bullet.rect):
                alien_bullets.remove(bullet)
                game_over = True

    # Draw everything
    player.draw()
    for bullet in bullets:
        bullet.draw()
    for bullet in alien_bullets:
        bullet.draw()
    for alien in aliens:
        alien.draw()
    
    # Draw UI elements
    pygame.draw.rect(screen, WHITE, (0, HEIGHT//2, WIDTH, 2))  # Middle line
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Level: {difficulty_level}", 10, 50)
    
    if game_over:
        draw_text("GAME OVER! Press R to restart", WIDTH//2 - 180, HEIGHT//2, RED)
        draw_text("Press M to return to Main Menu", WIDTH//2 - 190, HEIGHT//2 + 40, WHITE)
    
    pygame.display.update()

pygame.quit()