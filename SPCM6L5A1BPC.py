import math
import random    
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550
PLAYER_START_X = 365
PLAYER_START_Y = 375
ENEMY_START_Y_MIN = 55
ENEMY_START_Y_MAX = 170
ENEMY_SPEED_X = 0.5
ENEMY_SPEED_Y = 0.5
BULLET_SPEED_Y = 10
COLLISION_DISTANCE = 27

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background_image =pygame.transform.scale(pygame.image.load("background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Space Invaders")

player_image = pygame.transform.scale(pygame.image.load("player.png"), (60, 60))
player_x = PLAYER_START_X
player_y = PLAYER_START_Y
player_x_change = 0

enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6


for _i in range(number_of_enemies):
    enemy_image.append(pygame.transform.scale(pygame.image.load("enemy.png"), (60, 60)))
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 60))
    enemy_y.append(random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX))
    enemy_x_change.append(ENEMY_SPEED_X)
    enemy_y_change.append(ENEMY_SPEED_Y)


bullet_image = pygame.transform.scale(pygame.image.load("bullet.png"), (80, 80))
bullet_x = 0
bullet_y = PLAYER_START_Y
bullet_y_change = BULLET_SPEED_Y
bullet_state = "ready"
bullet_x_change = 0

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over():
    game_over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    return distance < COLLISION_DISTANCE


running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    player_x = max(0, min(player_x, SCREEN_WIDTH - 60))

    for i in range(number_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= SCREEN_WIDTH - 60:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]

        if enemy_y[i] > 340: 
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over()
            break

        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = PLAYER_START_Y
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 60)
            enemy_y[i] = random.randint(ENEMY_START_Y_MIN, ENEMY_START_Y_MAX)

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = PLAYER_START_Y
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
