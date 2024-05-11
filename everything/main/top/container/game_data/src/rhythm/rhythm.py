


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
########################################################################
try:   
    '''
    OK SO I CHALLENGED VINCENT TO MAKE A RHYTHM GAME AND NEED TO MAKE IT BEFORE END OF WEEKEND TUESDAY
    THE START DAY IS 4/5/24, FINISH BY FOLLOWING TUESDAY

    Goal:
        -So, here is what I intend to do. I am going to draw a rectangle on the bottom, visible.
        I am going to divide the top if the screen into an even amount, likely 8ths. 
        Squares will be drawn into one of these 8 positions. When they reach the bottom rectangle,
        you have to press the appropriate key.
            - keys can be (normal home typing pos): 
                - left: S, D, F
                - right: J, K, L
        Once you do, the cube will change color indicating it has been activated. 
        Once the cube is off of the screen, if it is activated, it will add to your score.
        It will also increase a streak. If it is not activated, it will reset your streak 
        and your score will go down.
        Music will be played in the background and somehow synced with these notes.
        
        GOALS:
            - fullscreen appliance, game built for 1080x1920 or whatever that resolution is
            - Get a good bakcground image
            - Get audio working and a map working
            - Get all required pygame things
            - Minimum delay for running as fast as possible (to not accidentally miss keys)
                - efficient cond statements    

        PYGAME NECESSARY:
            - delay:
                pygame.time.delay(10)

            - checking for events:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                    running = False

            - getting device inputs:
                keys = pygame.key.get_pressed()
                mouse = pygame.mouse.get_pressed()

            - rect with example inputs (must be one line in code):
                player = pygame.draw.rect(
                    window, 
                    color, 
                    (
                        x 
                        y, 
                        width, 
                        height
                    )
                )
                
        TODO:
            - NEED TO FIND OUT HOW TO MAP MUSIC INTO GAME, PREFERABLY FINAL PRODUCT IS A LIST
            - FIND OUT HOW TO PRELOAD AUDIO
            - COPY OVER CONCEPTS FROM FLAPPY BIRD
            - MAKE DYNAMIC CUBE GENERATION (2D array with a bool saying to generate a cube,
                and where to draw it (top left coord))
    '''

    # pip import for libraries
    # import pip
    # pip.main(['install', 'pygame'])
    # print('--------------------------')

    # other imports
    import pygame
    from pygame.locals import *
    import random
    import time
    import timeit
    import os
    import threading
    import json

    ### pygame 
    ## pygame
    # https://stackoverflow.com/questions/5814125/how-to-designate-where-pygame-creates-the-game-window
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    # W, H = pygame.display.Info().current_w, pygame.display.Info().current_h

    #######################################################################################

    ### CONSTANTS

    ## file name
    FILE_NAME = 'rhythm.py'
    ## screen
    # WIDTH = 1920 
    # HEIGHT = 1080
    pygame.init()
    WIDTH = pygame.display.Info().current_w
    HEIGHT = pygame.display.Info().current_h

    '''
    Everything that is dependent on screen dimensions:
    - bottom zone
    - notes width / height
    - time delay to handle how much to delay songs / notes for travel from top to bottom of screen
    '''

    ## a crapton of colors (thank you ChatGPT)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    ## environment, vscode (False), run (True)
    ENV = True

    ## active keys to register
    #REGISTER = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']
    REGISTER = [[0, K_s], [1, K_d], [2, K_f], [3, K_j], [4, K_k], [5, K_l]]
    DISPLAY_REGISTER = [[0, 'S'], [1, 'D'], [2, 'F'], [3, 'J'], [4, 'K'], [5, 'L']]
    #EXITS = [[K_LCTRL, K_c], [K_LCTRL, K_w], [K_ESCAPE]]

    #######################################################################################

    ### PRELOADING

    # establishing window 
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    #window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    pygame.display.set_caption("thing!")

    #######################################################################################

    ### functions

    ## func var
    paused = False
    # pausing?
    def pause_game():
        while paused:
            pass

    def scale(num: int, mode: int) -> int:
        if mode == 'x':
            return (num / 1920) * WIDTH
        
        elif mode == 'y':
            return (num / 1080) * HEIGHT
    ### classes

    class Data_format:
        def __init__(self):
            self.window = None
            self.color =  None
            self.x = None
            self.y = None
            self.width = None
            self.height = None
            self.state = None
        

    class Data:
        def __init__(self):
            self.active_cubes = []

        def iter(self):
            new_list = []
            for cubex in self.active_cubes:
                # old
                cubex.y += 1




                #new experimental scaling
                movement = 7.55 * dt * TARGET_FPS
                # print('moving by:', movement)
                cubex.y += movement







                if cubex.y < HEIGHT:
                    new_list.append(cubex)
                else:
                    points.reset_streak() # working
                    points.total += 1

            self.active_cubes = new_list

            # Remove cubes that have moved off the screen 
            #self.active_cubes = [cubex for cubex in self.active_cubes if cubex.y < HEIGHT]

        def add_to_active(self, obj):
            self.active_cubes.append(obj)


    class Profiles:
        '''
        SONGS
        - Boggle by Mega Mango
        - Loser, Baby (as per request) from Hazbin Hotel
        - Everybody Wants to Rule the World (tears for fears)

        MAP
        - Borderline by Tame Impala
        - Coconut mall, mario kart (7?)
        '''
        
        def __init__(self):
            
            ## class obj
            self.data = Data()

            ## constants
            self.CUBE_HEIGHT = scale(10, 'y')
            self.CUBE_WIDTH = scale(100, 'x')

            ## set up music player
            self.player = pygame.mixer
            self.player.init()

        def set(self):
            global ended
            ended = True

        def music_delay(self, time_amount, path):
            time_amount = scale(time_amount, 'y')
            time.sleep(time_amount)
            print('- music delay over, starting song.')
            self.player.music.load(path)
            self.player.music.set_volume(0.50)
            #self.player.music.set_volume(0.00)
            self.player.music.play()

        def secondary(self, right_time_track_list, right_track_list, color, sd, main_time):
            print('Secondary music thread started.')
            #print('--------------------------')
            
            ## vars
            # toggle when first starting, starts music and built-in delay
            starting_toggle = False
            sd = scale(sd, 'y')
            
            # main iter loop
            for times_right, track_right in zip(right_time_track_list, right_track_list):
                if times_right[0] == 'end':
                    pass
                else:
                    main_delay = round(times_right[0], 3)
                    main_delay_ms = int(main_delay * 1000)
                    if starting_toggle == True:
                        if paused == True:
                            while paused == True:
                                pass
                        elif paused == False:
                            time.sleep(main_delay)
                            x_val = notes.notes_pos[track_right]
                            obj = Data_format()
                            obj.window = window
                            obj.color = color
                            obj.x = x_val
                            obj.y = 0
                            obj.width = self.CUBE_WIDTH
                            obj.height = self.CUBE_HEIGHT
                            self.data.add_to_active(obj)
                    if starting_toggle == False:
                        start_delay = main_time - sd # secondary delay for ('timings_1_3-5')
                        start_delay_ms = int(1000 * start_delay)
                        time.sleep(start_delay)
                        print('- secondary sleep over, starting notes.')
                        starting_toggle = True
            print('Second playback done.')


        def Whats_the_Rush(self):
            print('--------------------------')
            print('Main music thread started.')
            ## preload files
            # get path to working directory
            # https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory
            wDir = os.path.dirname(os.path.abspath(__file__))
            if ENV:
                left_timing_path = os.path.join(wDir, "maps\\rush\\timings_1_0-5.json")
                left_track_path = os.path.join(wDir, "maps\\rush\\tracks_1_0-5.json")
                music_path = os.path.join(wDir, "songs_wav\\rush.wav")
            elif not ENV:
                left_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\rush\\timings_1_0-5.json"
                left_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\rush\\tracks_1_0-5.json"
                music_path = "main\\top\\game_data\\src\\rhythm\\songs_wav\\rush.wav"
            # load left time track
            print('Loading left timing track...')
            f = open(left_timing_path, 'r')
            left_time_track_list = json.load(f)
            f.close()
            # load left position track
            print('Loading left position track...')
            f = open(left_track_path, 'r')
            left_track_list = json.load(f)
            f.close()
            
            ## vars
            # toggle when first starting, starts music and built-in delay
            starting_toggle = False
            second_toggle = False
            print('--------------------------')
            print('Profile: "Whats the Rush?" by Jesse Woods')
            print('--------------------------')
            # main iter loop
            for times_left, track_left in zip(left_time_track_list, left_track_list):
                if times_left[0] == 'end':
                    pass
                else:
                    main_delay = round(times_left[0], 3)
                    main_delay_ms = int(main_delay * 1000)
                    if starting_toggle == True:
                        
                        if paused:
                            while paused:
                                print('player paused')

                        if second_toggle == False:
                            print('- music delay thread started.')
                            threading.Thread(target=lambda:self.music_delay(0.95, music_path)).start()
                            second_toggle = True

                        time.sleep(main_delay)
                        x_val = notes.notes_pos[track_left]
                        obj = Data_format()
                        obj.window = window
                        obj.color = BLUE
                        obj.x = x_val
                        obj.y = 0
                        obj.width = self.CUBE_WIDTH
                        obj.height = self.CUBE_HEIGHT
                        self.data.add_to_active(obj)
                    if starting_toggle == False:
                        # how long lyrics take to start - how long it takes square to travel down screen
                        #start_delay = 1.85 - 2.65 # delay for timings 1_0-5
                        start_delay = 0
                        start_delay_ms = int(1000 * start_delay)
                        print('Starting playback.')
                        print(f'- start delaying by {start_delay}s, {start_delay_ms}ms')
                        time.sleep(start_delay)
                        print('- main start delay over, starting notes')
                        starting_toggle = True
            print('Main playback done.')
            threading.Thread(target=lambda:self.state_eval(), daemon=True).start()

        def Stayed_Gone(self):
            print('--------------------------')
            print('Main music thread started.')
            #filename = os.path.join(wDir, 'setup/analyze.py')
            ## preload files
            # paths
            # get path to working directory
            # https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory
            wDir = os.path.dirname(os.path.abspath(__file__))
            if ENV:
                left_timing_path = os.path.join(wDir, "maps\\stayed_gone\\timings_3_0-2.json")
                left_track_path = os.path.join(wDir, "maps\\stayed_gone\\tracks_3_0-2.json")
                right_timing_path = os.path.join(wDir, "maps\\stayed_gone\\timings_1_3-5.json")
                right_track_path = os.path.join(wDir, "maps\\stayed_gone\\tracks_1_3-5.json")
                music_path = os.path.join(wDir, "songs_wav\\stayed_gone.wav")
            elif not ENV:
                left_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\stayed_gone\\timings_3_0-2.json"
                left_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\stayed_gone\\tracks_3_0-2.json"
                right_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\stayed_gone\\timings_1_3-5.json"
                right_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\stayed_gone\\tracks_1_3-5.json"
                music_path = "main\\top\\game_data\\src\\rhythm\\songs_wav\\stayed_gone.wav"
            # load left time track
            print('Loading left timing track...')
            f = open(left_timing_path, 'r')
            left_time_track_list = json.load(f)
            f.close()
            # load left position track
            print('Loading left position track...')
            f = open(left_track_path, 'r')
            left_track_list = json.load(f)
            f.close()
            print('Loading right timing track...')
            f = open(right_timing_path, 'r')
            right_time_track_list = json.load(f)
            f.close()
            print('Loading right posiition track...')
            f = open(right_track_path, 'r')
            right_track_list = json.load(f)
            f.close()
            #thread object
            secondary_thread = threading.Thread(target=lambda:self.secondary(right_time_track_list, right_track_list, RED, 2.50, 20.275))
            secondary_thread.start()
            
            ## vars
            # toggle when first starting, starts music and built-in delay
            starting_toggle = False
            print('--------------------------')
            print('Profile: "Stayed Gone" by Andrew Underberg, Sam Haft, Christian Borle, Amir Talai, and Joel Perez')
            print('--------------------------')
            # main iter loop
            for times_left, track_left in zip(left_time_track_list, left_track_list):
                if times_left[0] == 'end':
                    pass
                else:
                    main_delay = round(times_left[0], 3)
                    main_delay_ms = int(main_delay * 1000)
                    if starting_toggle == True:
                        if paused == True:
                            while paused == True:
                                pass
                        elif paused == False:
                            time.sleep(main_delay)
                            x_val = notes.notes_pos[track_left]
                            obj = Data_format()
                            obj.window = window
                            obj.color = BLUE
                            obj.x = x_val
                            obj.y = 0
                            obj.width = self.CUBE_WIDTH
                            obj.height = self.CUBE_HEIGHT
                            self.data.add_to_active(obj)
                    if starting_toggle == False:
                        self.player.music.load(music_path)
                        self.player.music.set_volume(0.50)
                        #self.player.music.set_volume(0.00)
                        self.player.music.play()
                        #start_delay = 20.775 # how long lyrics take to start - how long it takes square to travel down screen
                        # 20.275 - travel time
                        #start_delay = 20.275 - 2.75 # delay for timings_0-2.json
                        #start_delay = 20.275 - 2.25 # delay for ('vox vocals 1', 8).json
                        #start_delay = 20.275 - 2.70 # delay for ('vox vocals 1', 8).json
                        #start_delay = 20.275 - 2.70 # delay for timings_2_0-2
                        start_delay = 20.275 - scale(2.65, 'y') # delay for timings_3_0-2
                        start_delay_ms = int(1000 * start_delay)
                        print('Starting playback.')
                        print(f'- start delaying by {start_delay}s, {start_delay_ms}ms')
                        time.sleep(start_delay)
                        print('- main start delay over, starting notes')
                        starting_toggle = True
            print('Main playback done.')
            threading.Thread(target=lambda:self.state_eval(), daemon=True).start()

        def Rule_The_World(self):
            print('--------------------------')
            print('Main music thread started.')
            #filename = os.path.join(wDir, 'setup/analyze.py')
            ## preload files
            # paths
            # get path to working directory
            # https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory
            wDir = os.path.dirname(os.path.abspath(__file__))
            if ENV:
                # left_timing_path = os.path.join(wDir, "maps\\rule_the_world\\timings_1_0-5.json")
                # left_track_path = os.path.join(wDir, "maps\\rule_the_world\\tracks_1_0-5.json")
                left_timing_path = os.path.join(wDir, 'maps\\rule_the_world\\timings_2_0-5.json')
                left_track_path = os.path.join(wDir, 'maps\\rule_the_world\\tracks_2_0-5.json')
                music_path = os.path.join(wDir, "songs_wav\\rule_the_world.wav")
            elif not ENV:
                #left_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\rule_the_world\\timings_1_0-5.json"
                #left_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\rule_the_world\\tracks_1_0-5.json"
                left_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\rule_the_world\\timings_2_0-5.json"
                left_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\rule_the_world\\tracks_2_0-5.json"
                music_path = "main\\top\\game_data\\src\\rhythm\\songs_wav\\rule_the_world.wav"
            # load left time track
            print('Loading left timing track...')
            f = open(left_timing_path, 'r')
            left_time_track_list = json.load(f)
            f.close()
            # load left position track
            print('Loading left position track...')
            f = open(left_track_path, 'r')
            left_track_list = json.load(f)
            f.close()
            
            ## vars
            # toggle when first starting, starts music and built-in delay
            starting_toggle = False
            print('--------------------------')
            print('Profile: "Everybody Wants To Rule The World" by Tears for Fears')
            print('--------------------------')
            # main iter loop
            for times_left, track_left in zip(left_time_track_list, left_track_list):
                if times_left[0] == 'end':
                    pass
                else:
                    main_delay = round(times_left[0], 3)
                    main_delay_ms = int(main_delay * 1000)
                    if starting_toggle == True:
                        if paused == True:
                            while paused == True:
                                pass
                        elif paused == False:
                            time.sleep(main_delay)
                            x_val = notes.notes_pos[track_left]
                            obj = Data_format()
                            obj.window = window
                            obj.color = BLUE
                            obj.x = x_val
                            obj.y = 0
                            obj.width = self.CUBE_WIDTH
                            obj.height = self.CUBE_HEIGHT
                            self.data.add_to_active(obj)
                    if starting_toggle == False:
                        self.player.music.load(music_path)
                        self.player.music.set_volume(0.25)
                        #self.player.music.set_volume(0.00)
                        self.player.music.play()
                        #start_delay = 63.5 - scale(2.65, 'y') # delay for timings_1_0-5
                        # start_delay = 63.6 - scale(2.65, 'y') # delay for timings_1_0-5, with start thing
                        start_delay = 29.385 - scale(2.65, 'y') # delay for timings_1_0-5, with no start thing
                        start_delay_ms = int(1000 * start_delay)
                        print('Starting playback.')
                        print(f'- start delaying by {start_delay}s, {start_delay_ms}ms')
                        time.sleep(start_delay)
                        print('- main start delay over, starting notes')
                        starting_toggle = True
            print('Main playback done.')
            threading.Thread(target=lambda:self.state_eval(), daemon=True).start()

        def Boggle(self): 
            print('--------------------------')
            print('Main music thread started.')
            #filename = os.path.join(wDir, 'setup/analyze.py')
            ## preload files
            # paths
            # get path to working directory
            # https://stackoverflow.com/questions/21957131/python-not-finding-file-in-the-same-directory
            wDir = os.path.dirname(os.path.abspath(__file__))
            if ENV:
                left_timing_path = os.path.join(wDir, "maps\\boggle\\timings_1_0-5.json")
                left_track_path = os.path.join(wDir, "maps\\boggle\\tracks_1_0-5.json")
                music_path = os.path.join(wDir, "songs_wav\\boggle.wav")
            elif not ENV:
                left_timing_path = "main\\top\\game_data\\src\\rhythm\\maps\\boggle\\timings_1_0-5.json"
                left_track_path = "main\\top\\game_data\\src\\rhythm\\maps\\boggle\\tracks_1_0-5.json"
                music_path = "main\\top\\game_data\\src\\rhythm\\songs_wav\\boggle.wav"
            # load left time track
            print('Loading left timing track...')
            f = open(left_timing_path, 'r')
            left_time_track_list = json.load(f)
            f.close()
            # load left position track
            print('Loading left position track...')
            f = open(left_track_path, 'r')
            left_track_list = json.load(f)
            f.close()
            
            ## vars
            # toggle when first starting, starts music and built-in delay
            starting_toggle = False
            print('--------------------------')
            print('Profile: "Boggle" by Mega Mango')
            print('--------------------------')
            # main iter loop
            for times_left, track_left in zip(left_time_track_list, left_track_list):
                if times_left[0] == 'end':
                    pass
                else:
                    main_delay = round(times_left[0], 3)
                    main_delay_ms = int(main_delay * 1000)
                    if starting_toggle == True:
                        if paused == True:
                            while paused == True:
                                pass
                        elif paused == False:
                            time.sleep(main_delay)
                            x_val = notes.notes_pos[track_left]
                            obj = Data_format()
                            obj.window = window
                            obj.color = BLUE
                            obj.x = x_val
                            obj.y = 0
                            obj.width = self.CUBE_WIDTH
                            obj.height = self.CUBE_HEIGHT
                            self.data.add_to_active(obj)
                    if starting_toggle == False:
                        self.player.music.load(music_path)
                        self.player.music.set_volume(0.50)
                        #self.player.music.set_volume(0.00)
                        self.player.music.play()
                        start_delay = 29 - scale(2.65, 'y') # delay for timings_1_0-5 ################################################
                        start_delay_ms = int(1000 * start_delay)
                        print('Starting playback.')
                        print(f'- start delaying by {start_delay}s, {start_delay_ms}ms')
                        time.sleep(start_delay)
                        print('- main start delay over, starting notes')
                        starting_toggle = True
            print('Main playback done.')
            threading.Thread(target=lambda:self.state_eval(), daemon=True).start()

        def state_eval(self):
            state = self.player.music.get_busy()
            print('Awaiting song end... status:', state)
            while True:
                state = self.player.music.get_busy()
                if state == False:
                    if not self.player.music.get_busy():
                        self.set()
                        print('Song end recieved. Setting end')
                        break

        def prof_setup(self):
            # song lists
            self.song_dict = {
                "Stayed Gone": threading.Thread(target=lambda:self.Stayed_Gone(), daemon=True), # Stayed Gone
                "Whats the Rush?": threading.Thread(target=lambda:self.Whats_the_Rush(), daemon=True), # Whats the Rush
                "Everybody Wants To Rule The World": threading.Thread(target=lambda:self.Rule_The_World(), daemon=True), # Everybody Wants to Rule the World
                "Boggle": threading.Thread(target=lambda:self.Boggle(), daemon=True) # Boggle
            }


    class Notes:
        def __init__(self):
            # profiles class
            self.profiles = Profiles()

            self.notes_pos = []
            self.num_cubes = 6
            self.cube_width = self.profiles.CUBE_WIDTH  # Adjust this as needed

            # Calculate the gap between each cube
            self.gap = (WIDTH - (self.num_cubes * self.cube_width)) / (self.num_cubes + 1)

            # Calculate the x-coordinate for each cube
            for i in range(self.num_cubes):
                self.cube_x = (i + 1) * self.gap + i * self.cube_width
                self.notes_pos.append(self.cube_x)


    class Points:
        def __init__(self):
            self.total_points = 0
            self.streak = 0
            self.total = 0
            self.score_color = WHITE
        
        def reset_streak(self):
            self.streak = 0
        
        def point_up(self):
            self.total_points += 1
            self.streak += 1
        
        # def point_down(self):
        #     self.total_points -= 1



    class Draw:
        def __init__(self):
            self.draw_list = []
            self.text_list = []

        def draw(self):
            for obj in self.draw_list:
                # metallic gold:(211,175,55)
                # yellow: const YELLOW
                if obj.state != 'Div':
                    pygame.draw.rect(obj.window, end_screen.zone_color, (obj.x, obj.y, obj.width, obj.height)) # color used to be obj.color
                else:
                    pygame.draw.rect(obj.window, obj.color, (obj.x, obj.y, obj.width, obj.height)) # color used to be obj.color
            for obj in self.text_list:
                msg = font.render(str(obj[0]), True, end_screen.txt_color, None)
                window.blit(msg, obj[1])


    class Text: 
        def __init__(self, zone_x, zone_y, zone_width, zone_height):
            # div stuff
            self.pos = []
            self.num_txt = 6
            self.txt_width = scale(100, 'x')

            self.gap = (WIDTH - (self.num_txt * self.txt_width)) / (self.num_txt + 1)

            # zone stuff
            self.zx = zone_x
            self.zy = zone_y
            self.zw = zone_width
            self.zh = zone_height

            # Calculate the gap between each cube
            self.move_up = scale(75, 'y')
        
        def append(self):
            txt_size = scale(36 * 1.5, 'x')
            font = pygame.font.Font('freesansbold.ttf', round(txt_size))

            for i in range(self.num_txt):
                active_letter = DISPLAY_REGISTER[i][1]
                text = font.render(str(active_letter), True, WHITE, None)

                self.txt_x = (i + 1) * self.gap + i * self.txt_width
                self.txt_y = HEIGHT - self.move_up

                txt_rect = text.get_rect()
                txt_rect.center = (self.txt_x + self.txt_width / 2, self.txt_y)
                self.pos.append([active_letter, txt_rect])
            return self.pos



    class Div:
        def __init__(self):
            # class object
            self.draw = Draw()

            # div stuff
            self.divs_pos = []
            self.num_divs = 5
            self.div_width = 10  # Adjust this as needed

            # Calculate the gap between each cube
            self.gap = (WIDTH - (self.num_divs * self.div_width)) / (self.num_divs + 1)

        def append(self):
            for i in range(self.num_divs):
                self.move_up = 150

                self.cube_x = (i + 1) * self.gap + i * self.div_width
                
                self.height = HEIGHT - (HEIGHT - self.move_up)

                self.obj = Data_format()
                self.obj.window = window
                self.obj.color = WHITE
                self.obj.x = self.cube_x
                self.obj.y = HEIGHT - self.move_up
                self.obj.width = self.div_width
                self.obj.height = self.height
                self.obj.state = 'Div'
                #print('Adding dividers to background draw list...')
                #self.draw.draw_list.append(self.obj)
            


    class Zone:
        def __init__(self):
            # class objects
            self.div = Div()

            #vals to change
            self.move_up = scale(150, 'y')
            #self.move_up = 150
            
            # math (local)
            extra = HEIGHT - self.move_up
            gap = HEIGHT - extra

            # pos
            self.x = 0
            self.y = HEIGHT - self.move_up

            # size
            self.width = WIDTH
            self.height = gap

        def append(self):
            # set up draw object
            self.obj = Data_format()
            self.obj.window = window
            self.obj.color = YELLOW
            self.obj.x = self.x
            self.obj.y = self.y
            self.obj.width = self.width
            self.obj.height = self.height
            #print('Adding zone to bg draw list...')
            self.div.draw.draw_list.append(self.obj)
        
        def draw(self):
            #self.div.draw.draw_list.append(self.obj)
            #self.zone_rect = pygame.draw.rect(window, YELLOW, (self.x, self.y, self.width, self.height))
            self.zone_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        def dump_text(self):
            zone_text = Text(zone_x = zone.x, zone_y = zone.y, zone_width = zone.width, zone_height = zone.height)
            self.div.draw.text_list = zone_text.append()

        def handler(self):
            self.append()   
            self.draw()
            self.dump_text()
            self.div.append()


    class EndScreen:
        def __init__(self):
            self.draw_queue = []
            self.rect_color = (0, 0, 0)
            self.zone_color = (211,175,55) # metallic gold: #D4AF37
            self.txt_color = (255, 255, 255)

        def reset_mouse(self):
            pygame.mouse.set_visible(True)
            pygame.mouse.set_pos(mouse_pos[0] - 1, mouse_pos[1] - 1)

        def body_to_queue(self):
            self.width = scale(900, 'x')
            self.height = scale(500, 'y')
            self.x = WIDTH / 2 - self.width / 2
            self.y = HEIGHT / 2 - self.height / 2
            self.rect_obj = pygame.Rect(self.x, self.y, self.width, self.height)
            self.draw_queue.append(['rect', self.rect_obj])

        def iter_color(self):
            amount = 2
            am2 = 5
            goTo = False
            while True:
                #if self.color[0] < 254: # 255/5 = 51 steps to get white
                if self.rect_color[0] < 127: # 128/2 = 64 steps to get grey
                    self.rect_color = (self.rect_color[0] + amount, self.rect_color[1] + amount, self.rect_color[2] + amount)
                
                # fades score out?
                if points.score_color[0] > 0:
                    points.score_color = (points.score_color[0] - am2, points.score_color[1] - am2, points.score_color[2] - am2)
                
                # fades bottom text
                if self.txt_color[0] > 0:
                    self.txt_color = (self.txt_color[0] - 5, self.txt_color[1] - 5, self.txt_color[2] - 5)

                # I am not sure how any of this works but it makes zone end after its over so
                if self.zone_color[0] > 9:
                    n1 = self.zone_color[0] - 10
                if self.zone_color[1] > 5:
                    n2 = self.zone_color[1] - 6
                if self.zone_color[2] > 4:
                    n3 = self.zone_color[2] - 5
                else:
                    goTo = True
                self.zone_color = (n1, n2, n3)

                if goTo:
                    n1 = False
                    n2 = False
                    n3 = False
                    if self.zone_color[0] > 0:
                        n1 = True
                    else:
                        n1 = 0
                    if self.zone_color[1] > 5:
                        n2 = True
                    else:
                        n2 = 0
                    if self.zone_color[2] > 0:
                        n3 = True
                    else:
                        n3 = 0
                    
                    if n1 == True:
                        n1 = self.zone_color[0] - 1
                    if n2 == True:
                        n2 = self.zone_color[1] - 1
                    if n3 == True:
                        n3 = self.zone_color[2] - 1
                    self.zone_color = (n1, n2, n3)

                if self.rect_color[0] == 128 and points.score_color[0] == 0 and self.zone_color[0] == 0 and self.txt_color[0] == 0:
                    break
                time.sleep(0.0025)

        def text_to_queue(self):
            msg1 = f"Total score: {points.total_points} / {points.total}"
            txt1 = font.render(msg1, None, BLACK, None)
            txt_rect1 = txt1.get_rect()
            txt_rect1.center = (self.x + self.width / 2, self.y + 1.25 * (self.height / 4))

            msg2 = f"Streak: {points.streak}"
            txt2 = font.render(msg2, None, BLACK, None)
            txt_rect2 = txt2.get_rect()
            txt_rect2.center = (self.x + self.width / 2, self.y + 2.25 * (self.height / 4))
            
            self.draw_queue.append(['txt', txt1, txt_rect1])
            self.draw_queue.append(['txt', txt2, txt_rect2])

        def button_to_queue(self):
            width = self.width
            height = self.height
            x = self.x
            y = self.y

            x += width / 10
            y += 3 * (height / 4)

            width -= (2 * (width / 10))
            height -= (8.5 * (height / 10))

            self.button_obj = pygame.Rect(x, y, width, height)
            self.draw_queue.append(['button', (64, 64 ,64), self.button_obj])

        def display_handler(self):
            print('--------------------------')
            print('End screen invoked')
            time.sleep(3) # originally 5
            self.reset_mouse()
            self.body_to_queue()
            self.iter_color()
            time.sleep(0.25)
            self.text_to_queue()
            self.button_to_queue()
            print('End screen over')
            print('--------------------------')



    class Env:
        def __init__(self):
            self.count = 0

        def analyze(self):
            goal = 3
            self.prev_mouse_pos = mouse_pos
            while True:
                if mouse_pos == self.prev_mouse_pos:
                    if self.count < goal:
                        self.count += 1

                else:
                    self.count = 0
                    pygame.mouse.set_visible(True)

                self.prev_mouse_pos = mouse_pos
                if self.count == goal:
                    pygame.mouse.set_visible(False)
                    pygame.mouse.set_pos(mouse_pos[0] + 1, mouse_pos[1] + 1)
                time.sleep(1)
                

    #######################################################################################
    ## set up class objects
    points = Points()
    end_screen = EndScreen()
    zone = Zone()
    zone.handler()
    notes = Notes()

    mouse_pos = pygame.mouse.get_pos()
    env = Env()

    ## NEW ADDITION - before loading song profile, allow them to select
    # run display menu
    import tools.song_select as ss
    chosen_song = ss.display_loop()

    # restart vars
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("thing!")

    # get dict entry
    notes.profiles.prof_setup()
    try:
        ct = notes.profiles.song_dict[chosen_song] # ct = chosen thread
        ct.start()
    except:
        exit()

    # end thread
    et = threading.Thread(target=lambda:end_screen.display_handler(), daemon=True)

    # mouse detection thread
    pygame.mouse.set_visible(False)
    mst = threading.Thread(target=lambda:env.analyze(), daemon=True)
    if not mst.is_alive():
        mst.start()


    # set up clock (not used)
    clock = pygame.time.Clock()

    # set up text font
    f_size = round(scale((36 * 1.5), 'x'))
    font = pygame.font.Font('freesansbold.ttf', f_size)

    # load booleans
    pressed1 = False
    pressed2 = False
    space_pressed = False
    ended = False
    et_start = False
    running = True

    # delta time uwu
    clock = pygame.time.Clock()
    FPS = 60
    TARGET_FPS = 60
    prev = time.time()



    while running:
        # timing (delta)
        clock.tick(FPS)
        #print(round(clock.get_fps(), 2))
        now = time.time()
        dt = now - prev
        prev = now

        # pygame.time.delay(1)

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # gathering input data
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        # exits if
        if keys[K_LCTRL]:
            if keys[K_c]:
                #music_thread.join()
                print('--------------------------')
                print('ctrl + c')
                running = False
            elif keys[K_w]:
                #music_thread.join()
                print('--------------------------')
                print('ctrl + w')
                running = False
        if keys[K_ESCAPE]:
            #music_thread.join()
            print('--------------------------') ####################################
            print('escape') ####################################
            running = False ####################################
            #notes.profiles.player.music.stop()
            #ended = True
        
        # pause if
        # if keys[K_SPACE]:
        #     if space_pressed == False:
        #         if paused == False:
        #             paused = True
        #             print('music paused')
        #             notes.profiles.player.music.pause()
        #         elif paused == True:
        #             paused = False
        #             notes.profiles.player.music.unpause()
        #         space_pressed = True
        # if not keys[K_SPACE]:
        #     space_pressed = False

        ## draws
        window.fill(BLACK)
        # draws the input zone at bottom
        zone.div.draw.draw()
        # iterates through list of notes
        for obj in notes.profiles.data.active_cubes:
            active_note = pygame.draw.rect(obj.window, obj.color, (obj.x, obj.y, obj.width, obj.height))
            
            # only do if not paused
            if paused == False:
                # gets collumn of notes
                index = notes.notes_pos.index(obj.x)
                for i in REGISTER:
                    active_num1 = REGISTER.index(i)
                    if index == REGISTER[active_num1][0]:
                        active_key = REGISTER[active_num1][1]
                        break

                # checks if note is within zone
                if active_note.colliderect(zone.zone_rect):
                    # checks if the right key is pressed, if so remove note from list and increase points by 1
                    if keys[active_key]:
                        #if pressed1 == False: #############
                        notes.profiles.data.active_cubes.remove(obj)
                        points.total += 1
                        points.point_up()

        if ended:
            for item in end_screen.draw_queue:
                if item[0] == 'rect':
                    pygame.draw.rect(window, end_screen.rect_color, item[1])
                elif item[0] == 'txt':
                    window.blit(item[1], item[2])
                elif item[0] == 'button':
                    pygame.draw.rect(window, item[1], item[2])
                
            try:
                if end_screen.button_obj.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0]:
                        running = False
            except:
                pass




        # generate text for points
        txt_msg = f'{points.streak} | {points.total_points} | {points.total}'
        text = font.render(txt_msg, True, points.score_color, None) # text, some bool(?), text color, bg color
        # draw text
        text_rect = text.get_rect()
        tr_x = WIDTH / 2 # originally was just 75
        tr_y = 50
        tr_y = scale(tr_y, 'y')
        text_rect.center = (tr_x, tr_y)
        window.blit(text, text_rect)

        if ended:
            if not et.is_alive() and not et_start:
                et.start()
                et_start = True

        if paused == False:
            notes.profiles.data.iter()
        pygame.display.update()

    '''
    text = font.render(str(level), True, white, None) # text, some bool(?), text color, bg color
    text_rect = text.get_rect()
    text_rect.center = (25, 30) # some positioning
    window.blit(text, text_rect)
    '''

    pygame.quit()
    ct.join(timeout=0)

except Exception as e:
    import os
    import traceback
    Crash_Handler(
        wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        error = traceback.format_exc()
    )