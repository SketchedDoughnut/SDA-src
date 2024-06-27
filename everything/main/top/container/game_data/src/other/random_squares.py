import pygame
from pygame.locals import *
import random 
import time

pygame.init()
window = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('thing!')

## https://www.geeksforgeeks.org/how-to-draw-rectangle-in-pygame/
# Initializing Color
color1 = (255,0,0) # red
color2 = (0,255,0) # green
color3 = (0,0,255) # blue

count = {
    "red": 0,
    "green": 0,
    "blue": 0,
    "random": 0
}


# Drawing Rectangle
def draw():
    #window.fill((0, 0, 0))
    choice = random.randint(1,4)
    color4 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    if choice == 1:
        pygame.draw.rect(window, color1, pygame.Rect(random.randint(0, 1200), random.randint(0, 800), 60, 60))
        count['red'] += 1

    elif choice == 2:
        pygame.draw.rect(window, color2, pygame.Rect(random.randint(0, 1200), random.randint(0, 800), 60, 60))
        count['green'] += 1

    elif choice == 3:
        pygame.draw.rect(window, color3, pygame.Rect(random.randint(0, 1200), random.randint(0, 800), 60, 60))
        count['blue'] += 1

    elif choice == 4:
        pygame.draw.rect(window, color4, pygame.Rect(random.randint(0, 1200), random.randint(0, 800), 60, 60))
        count['random'] += 1

    print(count)
    pygame.display.flip()
    pygame.display.update()

def clear():
    window.fill((0, 0, 0))

running = True

# function calls go in here
while running:
    draw()

    # pygame events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_x:
                window.fill((0, 0, 0))
                for i in count:
                    count[i] = 0

            if event.key == K_SPACE:
                print('pause')