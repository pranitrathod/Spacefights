import pygame
import random
import math


# initials the pygame
pygame.init()

# Creating Background Image
background = pygame.image.load('309.jpg')
# create screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon setting
pygame.display.set_caption("Space Fight")  # this is used for title
icon = pygame.image.load('bullet.png')  # this is used to load image to titlebar
pygame.display.set_icon(icon)  # displaying icon

# Player/Spaceship here

playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 500
playerX_change = 0
playerY_change = 0

# Enemy  here
enemyImg = []
enemyX = []
enemyY = []
enemyX_speed = []
enemyY_speed = []
global no_of_enemy_increase
no_of_enemy_increase=6
global num_of_enemies
num_of_enemies = 80

# [num_of_enemies] This is because if we dont declare this then index get out of range and get an error as
#number of enemies are 80 but will increase from 6 to 79 or less then that

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monsters.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_speed.append(2)
    enemyY_speed.append(50)

# Bullet here

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 20
bullet_state = "ready"

# Score here
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 30)

textX = 10
textY = 10

# Game Over Font
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# GAME LEVEL
level_game = pygame.font.Font('freesansbold.ttf', 32)
level = 1


# GAMES FUNCTIONS TO DRAW THE IMAGES ON SCREEN WITH THE HELP OF
# screen.blit()

def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_the_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 1, y + 10))


def enemyDestory(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + ((math.pow(enemyY - bulletY, 2))))
    if distance < 27:
        return True


def show_scores(x, y):
    score = score_font.render('Scores:' + str(score_value), True, (250, 250, 250))
    screen.blit(score, (x, y))


def game_over():
    game = game_over_font.render('GAME OVER', True, (250, 250, 250))
    screen.blit(game, (200, 250))


def game_level():
    game_level = level_game.render('LEVEL:' + str(level), True, (250, 250, 250))
    screen.blit(game_level, (650, 10))


# GAME LOOP
running = True
while running:
    # RBG COLOR for Background
    # REMEMBER THE SCREEN IS FIRST DRAWN THEN BACKGROUND IMAGE AND ALL
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        # for window exit event
        if event.type == pygame.QUIT:
            running = False

        # FOR KEY MOVEMENTS
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -5.5
        # if event.key == pygame.K_UP:
        #    playerY_change = -0.2
        elif event.key == pygame.K_DOWN:
            playerY_change = 5.5
        elif event.key == pygame.K_RIGHT:
            playerX_change = 5.5

            # bullet event here
        if event.key == pygame.K_SPACE:
            if bullet_state is "ready":
                bulletX = playerX
                fire_the_bullet(bulletX, bulletY)

    if event.type == pygame.KEYUP:
        playerX_change = 0
        playerY_change = 0

    # Logic for Player movement
    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    if playerY >= 510:
        playerY = 500

    # logic for bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_the_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    for i in range(0,no_of_enemy_increase):

        # Logic for Enemy Movements
        enemyX[i] += enemyX_speed[i]
        if enemyX[i] <= 0:
            enemyX_speed[i] = 2.5
            enemyY[i] += enemyY_speed[i]
        if enemyX[i] >= 736:
            enemyX_speed[i] = -2.5
            enemyY[i] += enemyY_speed[i]

        # Logic for Destorying Enemy
        destoryed = enemyDestory(enemyX[i], enemyY[i], bulletX, bulletY)
        if destoryed:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

        # GAME OVER LOGIC
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()

    # GAME LEVEL LOGIC HERE
    if (score_value == 1):
        level = 2
        no_of_enemy_increase=8
    if (score_value == 15):
        level = 3
        no_of_enemy_increase=12
    if (score_value == 30):
        level = 4
        no_of_enemy_increase=15
    if (score_value == 45):
        level = 5
        no_of_enemy_increase=20
    if (score_value == 60):
        level = 6
        no_of_enemy_increase=30

    if (score_value == 100):
        level = 7
        no_of_enemy_increase=0
        num_of_enemies = 0
        winner = pygame.font.Font('freesansbold.ttf', 64)
        player_wins = winner.render('YOU WIN', True, (250, 250, 250))
        screen.blit(player_wins, (250, 250))

    # CALLING PLAYER FUNTIONS
    player(playerX, playerY)

    show_scores(textX, textY)

    game_level()

    pygame.display.update()
