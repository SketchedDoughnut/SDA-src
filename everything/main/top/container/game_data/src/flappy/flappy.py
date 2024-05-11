    # imports
    # installs pygame because quirky (only will run once, otherwise requirements are satisfied)
    # ypip = True
    # npip = False
    # import pip
    # if ypip:
    #     pip.main(['install', 'pygame'])
    #     print('--------------------------')

    # if npip:
    #     pip.main(['uninstall', 'pygame'])
    #     print('--------------------------')
    #     exit()







class Crash_Handler:
    def __init__(self, wDir, error):
        print('------------------')
        print('Crash Handler setting up...')
        con = self.convert_path(wDir, '/')
        con = self.split_path(con)
        con = self.assemble_path(con)
        con = self.promote_path(con)
        print('Path formatted...')
        dumps_path = self.assemble_dir(con)
        print('Directory assembled...')
        con = self.get_data(dumps_path)
        self.dump_data(con, error)
        print('Data acquired, dumped...')
        print('------------------')
        print('Crash documented to:', f'{con}')
        print('------------------')
        input('Enter anything to exit: ')
        exit()

    def convert_path(self, path, mode):
        n_string = ''
        for letter in path:
            if mode == '/':
                if letter == '\\':
                    n_string += '/'
                else:
                    n_string += letter
            elif mode == '\\':
                if letter == '/':
                    n_string += '\\'
                else:
                    n_string += letter
        return n_string
    
    def split_path(self, path):
        n_string = ''
        n_list = []
        for letter in path:
            if letter == '/':
                n_list.append(n_string)
                n_string = ''
            else:
                n_string += letter
        while n_list[0] == " ":
            n_list.pop(0)
        return n_list
    
    def assemble_path(self, path_list):
        n_string = ''
        for word in path_list:
            n_string += word
            n_string += '/'
        return n_string
    
    def remove_n_path_index(self, path):
        path_list = self.split_path(path)
        path_list.pop(len(path_list) - 1)
        path = self.assemble_path(path_list)
        return path_list, path
    
    def promote_path(self, path):
        while True:
            path_list, path = self.remove_n_path_index(path)
            if path_list[len(path_list) - 1] == 'everything':
                break
        return path

    def assemble_dir(self, path):
        path += 'crash/dumps'
        return path
    
    def format_time(self):
        import time
        s = (time.ctime(time.time()))
        s = s.replace(':', '-')
        s = s.split()
        for __ in range(2):
            s.pop(0)
        n_string = ''
        for num in s:
            n_string += num
            if s.index(num) != len(s) -1:
                n_string += '_'
        return n_string

    def get_data(self, dumps_dir):
        import os
        import json
        time_val = self.format_time()
        nc_log = os.path.join(dumps_dir, f'crash_log_{time_val}.log')
        nc_log = self.convert_path(nc_log, '\\')
        return nc_log

    def dump_data(self, path, error):
        #import json
        f = open(path, 'w')
        #json.dump(error, f)
        f.write(error)
        f.close()
###################################################
try:

    import pygame
    from pygame.locals import *
    import random
    import time
    import os
    import threading

    # init
    pygame.init()
    print('--------------------------')

    # dimensions of screen
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h

    # window settings
    window = pygame.display.set_mode((w, h))
    pygame.display.set_caption("thing!")


    ###################################################


    # cube data
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
    #level = 0


    # wall data
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
            self.y = random.randint(int(self.b_pos), h + 10)
            

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
            self.t_pos -= random.randint(0, int(h / 4))

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


    # enable or disable challenge mode: data
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
    # initialize cube
    cube = Cube()
    cube.pick_color()

    # initialize wall  1
    wall_1 = Walls()
    wall_1.pick_color()
    wall_1.b_vertical()

    # initialize wall 2
    wall_2 = Walls()
    wall_2.pick_color()
    wall_2.t_vertical(wall_1.y)

    #initialize challenge
    challenge = Challenge()

    # (duplicate) initializing level
    level = 0
    ###################################################


    # environment stuff
    # used to be class
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

        #re-initialize challenge
        # challenge = Challenge()

        # main loop vars / cases
        space_pressed = False
        mouse_pressed = False
        running = True
        break_main = False

        # level
        level = 0

        # GAME LOOP
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

            # break running and control if
                if keys[K_c]:
                    print('ctrl + c')
                    break_main = True
                    running = False

            # break running and control if
            if keys[K_ESCAPE]:
                print('escape')
                break_main = True
                running = False

            # break running and control if
            if cube.moving == True:
                cube.gravity() #####################
                #cube.y = wall_1.y - (wall_1.gap / 2) - (cube.height / 2) #####################
        
            # start env movement
            if keys[K_SPACE]:
                if cube.moving == False:
                    print('starting wall generation, wall movement, cube movement')
                    cube.moving = True
        
            # pause env movement
            if keys[K_x]:
                cube.moving = False
        
            # cube jumping
            if keys[K_SPACE]:
                if cube.moving == True:
                    if space_pressed == False:
                        cube.jumping()
                        space_pressed = True
            
            if not keys[K_SPACE]:
                space_pressed = False

            # extra jumping code, remove later #################################
            # if keys[K_c] or keys[K_v]:
            #     if cube.moving == True:
            #         if space_pressed == False:
            #             cube.jumping()
            #             space_pressed = True
                        
            # if not keys[K_c] or keys[K_v]:
            #     space_pressed = False
        
            # checking all mouse presses here
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

            # updating cube location
            if cube.moving == True:
                cube.update_location()
        
            # generating new walls if
            if wall_1.x < (-5 + (-1 * wall_1.width)) and wall_2.x < (-5 - (1 * wall_2.width)):
                print('generating new walls')
                wall_1 = Walls()
                wall_1.pick_color()
                wall_1.b_vertical()
        
                wall_2 = Walls()
                wall_2.pick_color()
                wall_2.t_vertical(wall_1.y)
        
                level += 1
                print(f'level up: {level}')
            
            if cube.moving == True:
                wall_1.move_wall()
                wall_2.move_wall()
                bounds()
        
            # draw objects
            window.fill((0, 0, 0)) # black out screen
            player = pygame.draw.rect(window, cube.color, (cube.x, cube.y, cube.width, cube.height)) # cube 
            wall_r1 = pygame.draw.rect(window, wall_1.color, (wall_1.x, wall_1.y, wall_1.width, wall_1.height)) # bottom wall
            wall_r2 = pygame.draw.rect(window, wall_2.color, (wall_2.x, wall_2.y, wall_2.width, wall_2.height)) # top wall
            challenge_rect = pygame.draw.rect(window, challenge.color, (challenge.x, challenge.y, challenge.width, challenge.height)) # bottom left button

            ## font
            ## https://www.geeksforgeeks.org/python-display-text-to-pygame-window/#google_vignette
            black = (0, 0, 0)
            white = (255, 255, 255)
            text = font.render(str(level), True, white, None) # text, some bool(?), text color, bg color
            text_rect = text.get_rect()
            text_rect.center = (25, 30) # some positioning
            window.blit(text, text_rect)

            # collision with bottom wall
            # https://www.youtube.com/watch?v=BHr9jxKithk 
            if player.colliderect(wall_r1):
                print('wall impact: bottom')
                running = False
        
            # collision with top wall
            elif player.colliderect(wall_r2):
                print('wall impact: top')
                running = False
        
            # update display
            pygame.display.update() 

        # breaks out of control loop
        if break_main == True:
            break
        
        else:
            time.sleep(1)

    # quit if control and main loop
    pygame.quit()

except Exception as e:
    import os
    import traceback
    Crash_Handler(
        wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        error = traceback.format_exc()
    )