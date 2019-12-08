import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))

# Title & Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('UFO.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('Background.png')

# Player Image
playerImg = pygame.image.load('Player.png')
playerX = 368
playerY = 480
playerX_change = 0

# Enemy Image
enemyImg = pygame.image.load('Enemy.png')
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 32
number_of_enemies = 5

for i in range(number_of_enemies):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(10, 150))
    enemyX_change.append(random.choice([-2, 2]))

# Bullet Image
bulletImg = pygame.image.load('Bullet.png')
bulletX = 368
bulletY = 480
bulletY_change = -5
bullet_state = "Ready"

# Collision Image
boom = pygame.image.load('Boom.png')

# Game Over Font
game_over_font = pygame.font.Font('Mickey.TTF', 64)

control = 1


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y - 32))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY + 32, 2))
    if distance < 32:
        return True
    else:
        return False


def explode(x, y):
    screen.blit(boom, (x, y))


def text_loose():
    text_loose = game_over_font.render("YOU LOST", True, (255, 255, 255))
    screen.blit(text_loose, (200, 250))


def sound_loose():
    sound_loose = mixer.Sound('Loose.wav')
    sound_loose.set_volume(0.3)
    sound_loose.play()


def text_win():
    text_win = game_over_font.render("YOU WON", True, (255, 255, 255))
    screen.blit(text_win, (200, 250))


def sound_win():
    sound_win = mixer.Sound('Win.wav')
    sound_win.set_volume(0.3)
    sound_win.play()


# Game Loop
running = True
while running:
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Pressing Key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            elif event.key == pygame.K_RIGHT:
                playerX_change = 3
            elif event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bullet_sound = mixer.Sound('Shoot.wav')
                    bullet_sound.set_volume(0.5)
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(number_of_enemies):
        # Loose
        if enemyY[i] > 400:
            for j in range(number_of_enemies):
                enemyY[j] = -100
                enemyY_change = 0
            sound_loose()

        if enemyY[i] < 0:
            text_loose()

        # Enemy Movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change
        elif enemyX[i] > 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # explode(enemyX[i], enemyY[i])
            explosion_sound = mixer.Sound('Explosion.wav')
            explosion_sound.set_volume(0.5)
            explosion_sound.play()
            bulletY = playerY
            bullet_state = "Ready"
            change = enemyX[i]
            enemyX[i] = enemyX[number_of_enemies - 1]
            enemyX[number_of_enemies - 1] = change
            change = enemyY[i]
            enemyY[i] = enemyY[number_of_enemies - 1]
            enemyY[number_of_enemies - 1] = change
            change = enemyX_change[i]
            enemyX_change[i] = enemyX_change[number_of_enemies - 1]
            enemyX_change[number_of_enemies - 1] = change
            number_of_enemies -= 1

        enemy(enemyX[i], enemyY[i])

    # Win
    if number_of_enemies == 0 and control == 1:
        sound_win()
        control = 0

    if number_of_enemies == 0:
        text_win()

    # Bullet Movement
    if bullet_state == "Fire":
        bulletY += bulletY_change
        fire_bullet(bulletX, bulletY)
    if bulletY == 0:
        bullet_state = "Ready"

    player(playerX, playerY)

    pygame.display.update()
