import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Title and icon
pygame.display.set_caption("Space-War")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

# Background
background_img = pygame.image.load("space_bg_2.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT)).convert()

# Background music
mixer.music.load("GameMusic.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Fonts
font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
small_font = pygame.font.Font("freesansbold.ttf", 24)

# Player
player_img = pygame.image.load("space-invaders-1.png")
player_x = random.randint(100, 700)
player_y = 500
vel = 7
score = 0

# Enemies
enemy_img = []
enemy_x = []
enemy_y = []
enemy_xchange = []
enemy_ychange = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(f"enemy-{i}.png"))
    enemy_x.append(random.randint(0, 400))
    enemy_y.append(random.randint(0, 60))
    enemy_xchange.append(2.5)
    enemy_ychange.append(50)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = player_x
bullet_y = player_y
bullet_change = 10
bullet_state = "ready"

# Sound effects
bullet_sound = mixer.Sound("Shot_1.mp3")
hit_sound = mixer.Sound("EnemyCrash.mp3")
warning_sound = mixer.Sound("Warning.mp3")
game_over_sound = mixer.Sound("game-end.mp3")

# Game state
running = True
game_over = False
game_over_sound_played = False


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(ex, ey, bx, by):
    distance = math.sqrt((ex - bx) ** 2 + (ey - by) ** 2)
    return distance < 35


def score_show(x, y):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))


def show_game_over():
    # Stop background music and play the game-over music once.
    global game_over_sound_played

    if not game_over_sound_played:
        mixer.music.stop()
        game_over_sound.play()
        game_over_sound_played = True

    screen.blit(background_img, (0, 0))

    title = game_over_font.render("GAME OVER", True, (255, 80, 80))
    final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))
    restart_hint = small_font.render("Close the window to exit", True, (220, 220, 220))

    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))
    screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
    screen.blit(restart_hint, restart_hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))


# Game loop
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound.play()
                bullet_x = player_x
                bullet_y = player_y
                bullet_state = "fire"

    if game_over:
        show_game_over()
        pygame.display.update()
        continue

    screen.blit(background_img, (0, 0))

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= vel
    if keys[pygame.K_RIGHT]:
        player_x += vel

    player_width = player_img.get_width()
    player_height = player_img.get_height()

    if player_x < 0:
        warning_sound.play()
        player_x = 0
    if player_x > WIDTH - player_width:
        warning_sound.play()
        player_x = WIDTH - player_width

    # Increase enemy speed as the score rises
    base_speed = 2.5 + score * 0.05
    for j in range(num_of_enemies):
        if enemy_xchange[j] > 0:
            enemy_xchange[j] = base_speed
        else:
            enemy_xchange[j] = -base_speed

    # Enemy movement, collisions, and drawing
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_xchange[i]

        enemy_width = enemy_img[i].get_width()
        enemy_height = enemy_img[i].get_height()

        if enemy_x[i] <= 0:
            enemy_x[i] = 0
            enemy_xchange[i] = abs(enemy_xchange[i])
            enemy_y[i] += enemy_ychange[i]
        elif enemy_x[i] >= WIDTH - enemy_width:
            enemy_x[i] = WIDTH - enemy_width
            enemy_xchange[i] = -abs(enemy_xchange[i])
            enemy_y[i] += enemy_ychange[i]

        # Game over if an enemy touches the ship or reaches the bottom.
        enemy_rect = pygame.Rect(enemy_x[i], enemy_y[i], enemy_width, enemy_height)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        if enemy_rect.colliderect(player_rect) or enemy_y[i] + enemy_height >= HEIGHT:
            game_over = True
            break

        # Bullet collision
        if bullet_state == "fire" and is_collision(
            enemy_x[i], enemy_y[i], bullet_x, bullet_y
        ):
            hit_sound.play()
            score += 1
            enemy_x[i] = random.randint(0, max(0, WIDTH - enemy_width))
            enemy_y[i] = random.randint(0, 60)
            enemy_xchange[i] = 2.5
            bullet_state = "ready"

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_change

        if bullet_y <= 0:
            bullet_state = "ready"
            bullet_x = player_x + (player_width // 2) - (bullet_img.get_width() // 2)
            bullet_y = player_y

    # Draw player and score while the game is active
    if not game_over:
        player(player_x, player_y)
        score_show(15, 15)

    pygame.display.update()

pygame.quit()
