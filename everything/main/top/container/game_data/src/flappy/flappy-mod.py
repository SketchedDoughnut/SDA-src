# imports
# installs pygame because quirky (only will run once, otherwise requirements are satisfied)
# rpip = True
# if rpip:
#     import pip
#     pip.main(['install', 'pygame'])

import pygame
from pygame.locals import *
import random
import time
import os
import threading

# init
pygame.init()

# dimensions of screen
w, h = pygame.display.Info().current_w, pygame.display.Info().current_h

# window settings
window = pygame.display.set_mode((w, h))
pygame.display.set_caption("thing!")


###################################################


# cube
class Cube:
    def __init__(self, jump=-10.5):

        # positionhttps://youtu.be/Ir5u9L4VZOo?list=PL3tRBEVW0hiDR4Q_ELqHvxcDqd4uvzbeO&t=110

        self.x = 500
        self.y = h / 2

        # sizing
        self.width = 40
        self.height = 40

        # motion
        self.yv = 0
        self.moving = False

        # environment
        self.grav = 0.5
        self.jump = jump

    ## functions aided by friend
    
    # pick color
    def pick_color(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 

    # generate gravity on cube
    def gravity(self, sub=0):
        self.yv += self.grav
        self.yv -= sub
    
    # update cubes location
    def update_location(self):
        self.y += self.yv 

    # make cube jump
    def jumping(self):
        self.yv = self.jump


###################################################
        
# leveling, defined below when objects for walls and cubes are made
level = 0

# wall
class Walls:
    def __init__(self):

        # position
        self.x = w
        self.gap = 200
        #self.gap = 10

        # sizing
        self.width = 100
        #self.height = 550  
        #self.height = 1100
        self.height = h


    def b_vertical(self):
        #self.y = h
        #self.y -= h / random.randint(1, 10)
        ####### attempt changes below  
        self.b_pos = h / 2
        self.b_pos = self.b_pos / 2
        #self.y = random.randint(self.b_pos + self.b_pos / 2, h)
        self.y = random.randint(self.b_pos, h + 10)
        

    def t_vertical(self, top_y):
        #self.y = h
        #self.y = 0.025 * (h / 10)
        ####### attempt changes below 
        # self.t_pos = h / 2
        # self.y = random.randint(0 + self.t_pos / 2, self.t_pos)
        # self.y += self.gap - self.height
        ####### new version below

        self.t_pos = top_y # sets position to y of first wall
        #print(top_y)
        #print(f'w1 pos: {self.t_pos}')
        self.t_pos -= self.gap # goes up by gap
        #print(self.gap)
        #print(f'gap: {self.t_pos}')
        self.t_pos -= self.height # goes up by height 
        #print(self.height)
        #print(f'height: {self.t_pos}')
        # random ranging from 0 to wall_1.y - gap - height
        #print(-1 * (self.height), ',', top_y - self.height - self.gap)
        # self.t_pos -= random.randint(-1 * (self.height), top_y - self.height - self.gap)
        self.t_pos -= random.randint(0, h / 4)

        #print(f'rand: {self.t_pos}')
        self.y = self.t_pos
        #print(f'y: {self.y}')
        #exit()

    # movement
    def move_wall(self, distance=5):
        ## old incremental system
        # if level < 6:
        #     self.x -= distance
        # else:
        #     if level > 4:
        #         self.x -= distance + 1

        #     if level > 9:
        #         self.x -= distance + 2

        #     if level > 14:
        #         self.x -= distance + 3

        ## new incremental system
        if challenge.challenge == True:
            # *5 = for challenge, don't multiply for normal (imo slow) increase

            self.x -= distance + (level // 5) * 5 
        
        elif challenge.challenge == False:
            self.x -= distance + (level // 5)

    # pick color
    def pick_color(self):
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) 


###################################################
        
class Challenge:
    def __init__(self):
        # dimensions
        self.width = 30
        self.height = 30

        # colors
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.color = (self.white)

        # mode
        self.challenge = False
        
        # position
        self.x = 0
        self.y = h - self.height # h - 30

    def collisions(self):
        pos = pygame.mouse.get_pos()
        if challenge_rect.collidepoint(pos):
            if self.challenge == False:
                self.color = self.red
                self.challenge = True
            
            elif self.challenge == True:
                self.color = self.white
                self.challenge = False

    

###################################################
class setup:
    '''
    Everything that needs to be shared:
        - data_list
        - time_list
        - param
        - total
        - div
        - wall_1
        - wall_2

    Everything that needs to b reset:
        - data_list
        - time_list
        - total
    '''

    def __init__(self):
        self.data_list = []
        self.time_list = []
        self.total = 0
        self.div = 0

        self.wall_1 = Walls()
        self.wall_1.pick_color()
        self.wall_1.b_vertical()

        self.wall_2 = Walls()
        self.wall_2.pick_color()
        self.wall_2.t_vertical(wall_1.y)

    def setup(self, mode):
        if mode:
            self.param = 3000

        elif mode == False:
            self.param = int(input('Input max test value: '))

    def clear(self):
        self.data_list = []
        self.time_list = []
        self.total = 0
        self.div = 0

    def data(self):
        #print(data_list)
        # data_list.append(wall_1.y - wall_2.height)
        # for i in data_list:
        #     temp += i 
        # temp2 = temp / len(data_list)
        ####################################################### new system below
        self.data_list.append(self.wall_1.y - self.wall_2.height)
        self.total += self.wall_1.y - self.wall_2.height
        self.div = self.total / len(self.data_list)
        os.system('clear')
        print('----------------------------------------')
        print(f'Walls distance: {(self.wall_1.y - self.wall_2.height)}')
        print(f'Avg: {self.div}')
        print(f'Avg (r->2): {round(self.div, 2)}')
        print(f'Total tests: {len(self.data_list)}/{self.param}')
        print(f'Time elapsed: {self.time_list[0]} --> {time.strftime("%H:%M:%S")}')
        #print(len(self.data_list))
    
        return len(self.data_list)
    

    def psuedo(self):

        # https://www.freecodecamp.org/news/python-get-current-time/
        self.time_list.append(time.strftime("%H:%M:%S"))
        #start = int(time.strftime("%S"))
        self.start = time.time()

        while True:
            self.wall_1 = Walls()
            self.wall_1.pick_color()
            self.wall_1.b_vertical()

            self.wall_2 = Walls()
            self.wall_2.pick_color()
            self.wall_2.t_vertical(wall_1.y)
            
            if self.data() == self.param:
                self.time_list.append(time.strftime("%H:%M:%S"))
                #end = int(time.strftime("%S"))
                self.end = time.time()
                print('----------------------------------------')
                #print(f'{param} tests done; cancelling.')
                print(f'{self.param} tests done.')
                
                #https://www.geeksforgeeks.org/how-to-check-the-execution-time-of-python-script/
                #print("The time of execution of above program is:", (round(self.end-self.start, 2)) * 10**3, "ms, or:", (round(self.end-self.start, 2)), "s")
                print(f"""TIME:
        - {round((self.end-self.start, 2)) * 10**3} ms
        - {round((self.end-self.start, 2))} s
        - {round((self.end-self.start, 2)) / 60} m
        - {round(((self.end-self.start, 2)) / 60) / 60} h""")
                print('----------------------------------------')
                #exit()
                break

    def run(self, mode=False):
        self.setup(mode)
        self.clear()
        self.psuedo()


###################################################
# initialize cube
cube = Cube()
cube.pick_color()

# initialize walls
wall_1 = Walls()
wall_1.pick_color()
wall_1.b_vertical()

wall_2 = Walls()
wall_2.pick_color()
wall_2.t_vertical(wall_1.y)

#initialize challenge
challenge = Challenge()

# leveling
level = 0
###################################################

def bounds():
    global running
    if cube.y >= h:
        print('out of bounds: down')
        running = False

    elif cube.y <= 0:
        print('out of bounds: top')
        running = False

'''
- CUBE
        - height: {cube.height}
        - width: {cube.width}
        - jump: {cube.jump}
        - grav: {cube.grav}
        - color: {cube.color}
        - moving: {cube.moving}
'''

###################################################



class Pho:

    def __init__(self, h, w):
        self.h = h
        self.w = w

        # initialize cube
        #self.cube = Cube(jump = -3.75)
        self.cube = Cube()
        self.cube.pick_color()

        # initialize walls
        self.wall_1 = Walls()
        self.wall_1.pick_color()
        self.wall_1.b_vertical()

        self.wall_2 = Walls()
        self.wall_2.pick_color()
        self.wall_2.t_vertical(self.wall_1.y)

    def collisions(self):
        # check borders collision
        if self.cube.y > self.h:
            print(f'Out of bounds: bottom ({self.cube.y})')
            return False
            
        if self.cube.y < 0:
            print(f'Out of bounds: top ({self.cube.y})')
            return False
        
        
    def inputs(self):
        while True:
            input()
            if self.cube.moving == True:
                for i in range(2):
                    self.cube.jumping()


    def within(self):
        # calc if within walls
        if self.cube.y < self.wall_1.y:
            if self.cube.y > self.wall_2.y + self.wall_2.height:
                return True
            else:
                return False
        else:
            return False


    def pho(self):

        # leveling
        level = 1

        corrections = 0
        correct = []

        #obj = setup()
        #obj.run(True)

        gap = abs(self.wall_1.y - self.wall_2.y)
        gap -= self.wall_1.height

        num = random.randint(50, 450)
        #num = self.wall_1.y - gap / 2

        self.loop = True
        while self.loop:
            #time.sleep(0.01)
            pygame.time.delay(10)

            if self.cube.moving == False:
                input('Enter anything to start: ')
                print('self.starting wall generation, wall movement, cube movement')
                #self.inputsv = threading.Thread(target=self.inputs,)
                #self.inputsv.start()
                threading.Thread(target=lambda: self.inputs())
                self.cube.moving = True
            
            if self.cube.moving == True:
                #self.cube.gravity(sub=0.25)
                self.cube.gravity()

            if self.cube.moving == True:
                self.cube.update_location()

            self.cube.y = num #####################
            
            if self.wall_1.x < (-5 + (-1 * self.wall_1.width)) and self.wall_2.x < (-5 - (1 * self.wall_2.width)):
                print('generating new walls')
                self.wall_1 = Walls()
                self.wall_1.pick_color()
                self.wall_1.b_vertical()

                self.wall_2 = Walls()
                self.wall_2.pick_color()
                self.wall_2.t_vertical(self.wall_1.y)
                #data()  

                level += 1
                print(f'level up: {level}')

                # gap calc
                gap = abs(self.wall_1.y - self.wall_2.y)
                gap -= self.wall_1.height

                num = random.randint(50, 450) #####################
                #num = self.wall_1.y - gap / 2 #####################
            
            if self.cube.moving == True:
                #self.wall_1.move_wall(distance=2.5)
                #self.wall_2.move_wall(distance=2.5)
                self.wall_1.move_wall()
                self.wall_2.move_wall()
                if self.collisions() == False:
                    self.loop = False
                    exit()

                window.fill((0, 0, 0))
                player = pygame.draw.rect(window, self.cube.color, (self.cube.x, self.cube.y, self.cube.width, self.cube.height))   
                wall_r1 = pygame.draw.rect(window, self.wall_1.color, (self.wall_1.x, self.wall_1.y, self.wall_1.width, self.wall_1.height))     
                wall_r2 = pygame.draw.rect(window, self.wall_2.color, (self.wall_2.x, self.wall_2.y, self.wall_2.width, self.wall_2.height))    
                pygame.display.update() 

            # calc if within walls
            within = self.within()

            while within == False:
                t1 = self.cube.y
                for i in range(40, h - 40):
                    self.cube.y = i
                    print(f'Correcting... {self.cube.y}')
                    #time.sleep(0.025)
                    within = self.within()
                    if within:
                        break
                #print('number found')
                num = self.cube.y
                t2 = num
                correct.append([t1, t2])
                corrections += 1
            
            # os.system('clear')
            try:
                avg = level / corrections
            except:
                print('not enough cycles')
                avg = 0
            print(f"""----------------------------------------
DATA:
    ENV
        - height: {self.h}
        - width: {self.w}
    CUBE
        - x: {self.cube.x}
        - y: {self.cube.y}
        - height: {self.cube.height}
        - width: {self.cube.width}
        - grav: {self.cube.grav}
            - sub: {5}

    WALLS
        - gap: {gap}
        - total: 
        - dif from top of wall_1 to bottom of wall_2: 

    BOTTOM WALL (1)
        - x: {self.wall_1.x}
        - y: {self.wall_1.y}
        - b_pos: {self.wall_1.b_pos}
        - top: {self.wall_1.y}

    TOP WALL (2)
        - x: {self.wall_2.x}
        - y: {self.wall_2.y}
        - t_pos: {self.wall_2.t_pos}
        - bottom: {self.wall_2.y + self.wall_2.height}

    STATES
        - within gap: {within}
        - can fit in gap: {gap > 50}
        - gap conflict: {gap < self.wall_1.gap}
            {gap} < {self.wall_1.gap}?

    CYCLE: {level}
    CORRECTIONS: {corrections}
    AVG: {avg}
    THREADS: {threading.active_count()}
    CUBE Y: {self.cube.y}
----------------------------------------""")
            '''
            COLLISIONS
                - wy1: {self.wy1}
                - wb1: {self.wb1}
                - wy2: {self.wy2}
                - wb2: {self.wb2}
            '''
            if gap < self.wall_1.gap == False:
                print('Gap conflict found.')
                exit()
            if gap > 50 == False:
                print('Cube fit error found.')
                exit()



###################################################


# obj = setup()
# obj.run()
                
#pho = Pho(h=h, w=w)
#pho.pho()

## loads font(s)
## https://www.geeksforgeeks.org/python-display-text-to-pygame-window/#google_vignette
font = pygame.font.Font('freesansbold.ttf', 36)

# CONTROL LOOP
while True:
    #re-initialize cube
    cube = Cube()
    cube.pick_color()

    #re-initialize walls
    wall_1 = Walls()
    wall_1.pick_color()
    wall_1.b_vertical()
    wall_2 = Walls()
    wall_2.pick_color()
    wall_2.t_vertical(wall_1.y)

    #initialize challenge
    challenge = Challenge()

    # main loop vars / cases
    space_pressed = False
    mouse_pressed = False
    running = True
    break_main = False

    # level
    level = 0

    # MAIN GAME LOOP
    while running:
        # timer for delay
        pygame.time.delay(10)
    
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # check all keys here
        keys = pygame.key.get_pressed()
        if keys[K_LCTRL]: 
            if keys[K_w]:
                print('ctrl + w')
                break_main = True
                running = False

            if keys[K_c]:
                print('ctrl + c')
                break_main = True
                running = False

        if keys[K_ESCAPE]:
            print('escape')
            break_main = True
            running = False
    
        if cube.moving == True:
            cube.gravity() #####################
            # cube.y = wall_1.y - (wall_1.gap / 2) - (cube.height / 2) #####################
    
        if keys[K_SPACE]:
            if cube.moving == False:
                print('starting wall generation, wall movement, cube movement')
                #gap = abs(wall_1.y - wall_2.y)
                #gap -= wall_1.height
                #print(gap)
    
            cube.moving = True
    
        if keys[K_x]:
            cube.moving = False
    
        if keys[K_SPACE]:
            if cube.moving == True:
                if space_pressed == False:
                    cube.jumping()
                    space_pressed = True
        
        if not keys[K_SPACE]:
            space_pressed = False
    
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if mouse_pressed == False:
                try:
                    challenge.collisions()
                    mouse_pressed = True

                except Exception as e:
                    print(f'no rect yet: {e}')
        
        if not mouse[0]:
            mouse_pressed = False

        # functions
        if cube.moving == True:
            cube.update_location()
    
    
        #cube.pick_color()
    
        if wall_1.x < (-5 + (-1 * wall_1.width)) and wall_2.x < (-5 - (1 * wall_2.width)):
            print('generating new walls')
            wall_1 = Walls()
            wall_1.pick_color()
            wall_1.b_vertical()
    
            wall_2 = Walls()
            wall_2.pick_color()
            wall_2.t_vertical(wall_1.y)
            #print(wall_2.t_pos)
            #data()  
    
            #gap = abs(wall_1.y - wall_2.y)
            #gap -= wall_1.height
            #print(gap)
    
            level += 1
            print(f'level up: {level}')
        
        if cube.moving == True:
            wall_1.move_wall()
            wall_2.move_wall()
            bounds() 
    
        # make rect and update display
        window.fill((0, 0, 0))
        player = pygame.draw.rect(window, cube.color, (cube.x, cube.y, cube.width, cube.height))   
        wall_r1 = pygame.draw.rect(window, wall_1.color, (wall_1.x, wall_1.y, wall_1.width, wall_1.height))     
        wall_r2 = pygame.draw.rect(window, wall_2.color, (wall_2.x, wall_2.y, wall_2.width, wall_2.height))
        challenge_rect = pygame.draw.rect(window, challenge.color, (challenge.x, challenge.y, challenge.width, challenge.height))

        ## font
        ## https://www.geeksforgeeks.org/python-display-text-to-pygame-window/#google_vignette
        black = (0, 0, 0)
        white = (255, 255, 255)
        text = font.render(str(level), True, white, None)
        text_rect = text.get_rect()
        text_rect.center = (25, 30)
        window.blit(text, text_rect)

        # https://www.youtube.com/watch?v=BHr9jxKithk 
        if player.colliderect(wall_r1): 
            print('wall impact: bottom')
            running = False
    
        elif player.colliderect(wall_r2): 
            print('wall impact: top') 
            running = False
    
        pygame.display.update() 

    if break_main == True:
        break
    
    else:
        time.sleep(1)

# quit if exit loop
pygame.quit()
