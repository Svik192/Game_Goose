import pygame
import random
import os

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

HEIGT = 900
WIDTH = 1600

FONT = pygame.font.SysFont('Arial',32)
COLOR_LIFE = (255,0,0)
COLOR_SCORE = (0,0,255)
score = 0
life = 3


FPS = pygame.time.Clock()

main_display = pygame.display.set_mode((WIDTH, HEIGT))

bg = pygame.transform.scale(pygame.image.load('background.png'),(WIDTH, HEIGT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

heart = pygame.transform.scale(pygame.image.load('heart.png').convert_alpha(),(50, 50))
icon_score = pygame.transform.scale(pygame.image.load('box.png').convert_alpha(),(40, 40))

player = pygame.image.load('player.png').convert_alpha()
player_size = player.get_size()
player_rect  = player.get_rect()

player_rect.top = int((HEIGT-player_size[1])/2)
player_rect.left = WIDTH/10

speed_player = 7
player_move_down = [0,speed_player]
player_move_up = [0,-speed_player]
player_move_right= [speed_player,0]
player_move_left = [-speed_player,0]

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()

    enemy_size = enemy.get_size()
    scale = 1
    enemy = pygame.transform.scale(pygame.image.load('enemy.png'),(scale*enemy_size[0], scale*enemy_size[1]))
    enemy_size = enemy.get_size()
        
    enemy_rect  = pygame.Rect(WIDTH,random.randint(0,HEIGT-(1*enemy_size[1])), *enemy_size)

    enemy_move = [random.randint(-10,-8),0]

    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_size = bonus.get_size()
    scale = 1
    bonus = pygame.transform.scale(pygame.image.load('bonus.png'),(scale*bonus_size[0], scale*bonus_size[1]))
    bonus_size = bonus.get_size()

    bonus_rect  = pygame.Rect(random.randint(0,WIDTH-(1*bonus_size[0])),-bonus_size[0], *bonus_size)

    bonus_move = [0,random.randint(4,6)]

    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)


enemies = []
bonuses = []

image_index = 0

playing = True
while playing:
    FPS.tick(100)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append (create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append (create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
   
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg,(bg_X1,0))
    main_display.blit(bg,(bg_X2,0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    main_display.blit(player,player_rect)
    main_display.blit(FONT.render(str(score),True,COLOR_SCORE),((WIDTH-90),20))
    main_display.blit(icon_score,(((WIDTH-50),20)))

    main_display.blit(FONT.render(str(life),True,COLOR_LIFE),((WIDTH-90),60))
    main_display.blit(heart,(((WIDTH-50),55)))

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])


        if player_rect.colliderect(enemy[1]):
            enemies.pop (enemies.index(enemy))
            life -= 1

            if life == 0:
                playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop (bonuses.index(bonus))
            score += 1

  
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop (enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGT:
            bonuses.pop (bonuses.index(bonus))

