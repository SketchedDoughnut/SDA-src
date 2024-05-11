'''
so this is essentially just an imported file used for the start page to select songs
'''

# imports
import threading
import os
import time
import random

# pygame setup
import pygame
from pygame.locals import *

# dimensions
pygame.init()
# WIDTH = pygame.display.Info().current_w
# HEIGHT = pygame.display.Info().current_h
WIDTH = 1000 # changed to 1000
HEIGHT = 500

# essentials
# window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
window = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("thing!")

class Colors:
    def __init__(self):
        self.RED = [255, 0, 0]
        self.GREEN = [0, 255, 0]
        self.BLUE =[0, 0, 255]
        self.WHITE = [255, 255, 255]
        self.rand1 = [random.randint(100, 255), random.randint(25, 255), random.randint(70, 255)]
        self.rand2 = [random.randint(50, 255), random.randint(2, 255), random.randint(15, 255)]



class Format:
    def __init__(self):
        self.x = None
        self.y = None
        self.height = None
        self.width = None
        self.color = None



class Select:
    def __init__(self):

        # sets up profile info
        # self.profile_count = 3
        self.profiles = [['Stayed Gone', False], ['Whats the Rush?', False], ['Everybody Wants To Rule The World', False], ["Boggle", False]]
        self.profile_count = len(self.profiles)
        self.profiles_y = []

        # height of boxes 
        self.box_height = HEIGHT / self.profile_count

        # draw queue
        self.draw_queue = []
        self.rect_draw_queue = []
        self.text_draw_queue = []


    def div(self):
        # necessary?
        gap = (HEIGHT - (self.profile_count * self.box_height)) / (self.profile_count + 1) # Calculate the gap between each cube

        # calc top left box pos'
        for i in range(self.profile_count): # Calculate the y-coordinate for each cube
            cube_y = round((i + 1) * gap + i * self.box_height)
            self.profiles_y.append(cube_y)


    def add_to_queue(self):
        print('--------------------------')
        print('Colors selected: ') #
        for y in self.profiles_y:
            obj = Format()
            self.colors = Colors()
            obj.y = y
            obj.x = 0
            obj.width = WIDTH
            obj.height = self.box_height
            tmp_num = random.randint(1, 2)
            if tmp_num == 1:
                obj.color = self.colors.rand1
            elif tmp_num == 2:
                obj.color = self.colors.rand2
            print('-', obj.color) #
            self.draw_queue.append(obj)
    

    def assemble_rect(self):
        for obj in self.draw_queue:
            n_obj = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            self.rect_draw_queue.append(n_obj)


    def assemble_text(self):
        font = pygame.font.Font('freesansbold.ttf', round(36 * 1.5))
        for title in self.profiles:
            text = font.render(str(title[0]), True, self.colors.WHITE, None) # text, some bool(?), text color, bg color
            horizontal = WIDTH / 2
            vertical = (self.profiles.index(title) + 0.5) * (HEIGHT / self.profile_count)
            text_rect = text.get_rect(center=(horizontal, vertical))
            self.text_draw_queue.append([text, text_rect])


    def graceful_exit(self):
        global running
        for i in self.profiles:
            if i[1]:
                print('--------------------------')
                print(f'Returning selected song: {i[0]}')
                running = False
                return i[0]
            
    
    def handler(self):
        self.div()
        self.add_to_queue()
        self.assemble_rect()
        self.assemble_text()



running = True
def display_loop():
    global running, window
    global HEIGHT, WIDTH

    # funcs
    select = Select()
    select.handler()
    
    # main game loop
    while running:
        # delay
        pygame.time.delay(1)

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('window exit')
                running = False

            # https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame
            # if event.type == pygame.VIDEORESIZE:
            #     # There's some code to add back window content here.
            #     window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #     WIDTH = pygame.display.get_window_size()[0]
            #     HEIGHT = pygame.display.get_window_size()[1]
            #     print(WIDTH, HEIGHT)
            #     s2 = Select()
            #     s2.handler()

        # gathering input data
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # exits if
        if keys[K_LCTRL]:
            if keys[K_c]:
                print('--------------------------')
                print('ctrl + c')
                running = False
            elif keys[K_w]:
                print('--------------------------')
                print('ctrl + w')
                running = False
        if keys[K_ESCAPE]:
            print('--------------------------')
            print('escape')
            running = False

        window.fill((0, 0, 0))
        for obj, rect_obj, text_obj in zip(select.draw_queue, select.rect_draw_queue, select.text_draw_queue):
            tr = pygame.draw.rect(window, obj.color, rect_obj)
            window.blit(text_obj[0], text_obj[1])

            # check collisions
            locate = select.rect_draw_queue.index(rect_obj)
            index = select.profiles[locate]
            if tr.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    index[1] = True
                else:
                    index[1] = False
            #print(select.profiles)
            
        v = select.graceful_exit()

        pygame.display.update()

    #pygame.quit()
    return v

#print(display_loop())