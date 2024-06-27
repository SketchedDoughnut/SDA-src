import pygame
from pygame.locals import *

import random

pygame.init()

# https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-tutorial-movement
#screen_width = 500
#screen_height = 500

w, h = pygame.display.Info().current_w, pygame.display.Info().current_h

window = pygame.display.set_mode((w, h))
pygame.display.set_caption("thing!")

x = 50
y = 50
width = 40
height = 40
vel = 2.5

def borders(axis, vel, mode):
    if False:
        pass

    else:
        if mode == 'a':
            axis += vel

        elif mode == 's':
            axis -= vel

    #print(axis)
    return axis

color = (255, 255, 255)

run = True

while run:
    pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[K_LCTRL]:
        if keys[K_w]:
            run = False

        if keys[K_e]:
            window.fill((255, 0, 0))
        if keys[K_r]:
            window.fill((0, 255, 0))
        if keys[K_f]:
            window.fill((0, 0, 255))
        if keys[K_SPACE]:
            window.fill((255, 255, 255))
    
    #y += 1
    #color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if keys[K_x]:
        window.fill((0, 0, 0))

    if keys[K_a]:
        #x -= vel
        x = borders(x, vel, 's')

    if keys[K_d]:
        #x += vel
        x = borders(x, vel, 'a')

    if keys[K_w]:
        #y -= vel
        y = borders(y, vel, 's')

    if keys[K_s]:
        #y += vel
        y = borders(y, vel, 'a')

    
    # color changing
    if keys[K_e]:
        color = (255, 0, 0)
    if keys[K_r]:
        color = (0, 255, 0)
    if keys[K_f]:
        color = (0, 0, 255)
    if keys[K_SPACE]:
        color = (255, 255, 255)

    pygame.draw.rect(window, color, (x, y, width, height))   
    pygame.display.update() 
    
pygame.quit()