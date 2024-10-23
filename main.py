import pygame
import random
import math
import time  # Import time for the sleep function
from pygame import mixer

# initializing pygame
pygame.init()

# creating screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# caption and icon
pygame.display.set_caption("Space Invaders by Lil Mo")

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pygame.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


# Show score
def show_score(x, y):
    score = font.render("Points: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over display
def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


# Reset the game to the initial state
def reset_game():
    global player_X, player_Y, player_Xchange, invader_X, invader_Y, invader_Xchange, bullet_list, score_val, game_over_state
    player_X = 370
    player_Y = 523
    player_Xchange = 0

    for i in range(no_of_invaders):
        invader_X[i] = random.randint(64, 737)
        invader_Y[i] = random.randint(30, 180)
        invader_Xchange[i] = 1.2

    bullet_list.clear()  # Reset bullets
    score_val = 0
    game_over_state = False  # Ensure game_over_state is reset


# Background Sound
mixer.music.load('data/background.wav')
mixer.music.play(-1)

# player
playerImage = pygame.image.load('data/spaceship.png')
player_X = 370
player_Y = 523
player_Xchange = 0

# Invader
invaderImage = []
invader_X = []
invader_Y = []
invader_Xchange = []
invader_Ychange = []
no_of_invaders = 8

for num in range(no_of_invaders):
    invaderImage.append(pygame.image.load('data/alien.png'))
    invader_X.append(random.randint(64, 737))
    invader_Y.append(random.randint(30, 180))
    invader_Xchange.append(1.2)
    invader_Ychange.append(50)

# Bullet list (for multiple bullets)
bulletImage = pygame.image.load('data/bullet.png')
bullet_Ychange = 3
bullet_list = []


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distance <= 50:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImage, (x - 16, y + 10))


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


def bullet(x, y):
    screen.blit(bulletImage, (x, y))


# Create a clock object to manage the frame rate
clock = pygame.time.Clock()

# game loop
running = True
game_over_state = False  # Game over state
time.sleep(2)  # Add a 2-second delay before starting the game

# Keep track of key presses
keys_pressed = {"left": False, "right": False}

while running:
    clock.tick(60)  # Limit the game to 60 FPS

    # RGB
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Controlling the player movement with key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys_pressed["left"] = True
            if event.key == pygame.K_RIGHT:
                keys_pressed["right"] = True
            if event.key == pygame.K_SPACE and not game_over_state:
                # Shoot a new bullet regardless of current bullet state
                bullet_X = player_X
                bullet_Y = player_Y
                bullet_list.append([bullet_X, bullet_Y])
                bullet_sound = mixer.Sound('data/bullet.wav')
                bullet_sound.play()
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_RETURN and game_over_state:
                reset_game()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys_pressed["left"] = False
            if event.key == pygame.K_RIGHT:
                keys_pressed["right"] = False

    # Update player movement based on keys pressed
    if keys_pressed["left"]:
        player_Xchange = -1.7
    elif keys_pressed["right"]:
        player_Xchange = 1.7
    else:
        player_Xchange = 0

    # adding the change in the player position
    player_X += player_Xchange

    if not game_over_state:
        for i in range(no_of_invaders):
            invader_X[i] += invader_Xchange[i]

        # bullet movement
        for bullet_pos in bullet_list[:]:
            bullet(bullet_pos[0], bullet_pos[1])
            bullet_pos[1] -= bullet_Ychange  # Move bullet upwards
            if bullet_pos[1] < 0:  # Remove the bullet when it goes off screen
                bullet_list.remove(bullet_pos)

        # movement of the invader
        for i in range(no_of_invaders):
            if invader_Y[i] >= 450 and abs(player_X - invader_X[i]) < 80:
                for j in range(no_of_invaders):
                    invader_Y[j] = 2000
                    explosion_sound = mixer.Sound('data/explosion.wav')
                    explosion_sound.play()
                game_over_state = True
                break  # Once the game is over, exit the loop

            if invader_X[i] >= 735 or invader_X[i] <= 0:
                invader_Xchange[i] *= -1
                invader_Y[i] += invader_Ychange[i]

            # Check for collisions with each bullet
            for bullet_pos in bullet_list[:]:
                collision = isCollision(bullet_pos[0], invader_X[i], bullet_pos[1], invader_Y[i])
                if collision:
                    score_val += 1
                    bullet_list.remove(bullet_pos)
                    invader_X[i] = random.randint(64, 736)
                    invader_Y[i] = random.randint(30, 200)
                    invader_Xchange[i] *= -1

            invader(invader_X[i], invader_Y[i], i)

        # restricting the spaceship so it doesn't go out of screen
        if player_X <= 16:
            player_X = 16
        elif player_X >= 750:
            player_X = 750

        player(player_X, player_Y)
        show_score(scoreX, scoreY)

    if game_over_state:
        game_over()  # Display "Game Over" message after the game ends

    pygame.display.update()
