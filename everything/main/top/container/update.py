print('----------------------------')
import pygame
from pygame.locals import *
import json
import os
import requests
import time
import threading

'''
POSSIBLE SOURCES

https://stackoverflow.com/questions/60716016/how-to-get-the-latest-release-version-in-github-only-use-python-requests
https://gist.github.com/pdashford/2e4bcd4fc2343e2fd03efe4da17f577d
https://gist.github.com/jwodder/c0ad1a5a0b6fda18c15dbdb405e1e549
'''

'''
IDEAS

- make a way to create releases that are announcements that can be displayed in game
    - the name "!announce" will trigger it(?)
- create urgency indicators that will demand an update
- make a seperate branch / release tag for game_data and make it wipe and re-install it, KEEP IT SEPERATE FROM ACTUAL DATA (only re-install games)
- check installer version and warn if its out of date
- add a choices function that gets choices with two buttons, you can input: x, y, width, height
'''

'''
OUTLINE

- setup
- starts check for update as a thread
- pygame puts text (from global variable text_msg)
- if X on window, ctrl c, escape, ctrl w: run function as thread (w/ daemon) that loops, setting text_msg to: "Are you sure you want to cancel?", and set _cancel to true
    - if no, set _cancel to False, and join the above function thread
    - if yes, set exit to True, join all threads, have exit code outside of the loop
'''
# pygame
pygame.init()

WIDTH = 300
HEIGHT = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN  = (0, 255, 0)

text_msg = 'Checking for updates...'

_cancel = False
do_exit = False
confirm = False
update_exit = False

directory = 'x'

top_wDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'setup/data.json')
wDir = os.path.dirname(os.path.abspath(__file__))

# resetting state
f = open(f'{wDir}/state.json', 'w')
json.dump(False, f)
f.close()
################################################################################################

# runs as a thread, checks version while pygame cheeks drawing
def check_version():
    # globals
    global do_exit, text_msg, confirm, _cancel, text_height, directory

    '''
    RUNDOWN
    - check for if latest version does not match current version
    '''

    # release destination, working directory, loading version
    #dest = 'https://api.github.com/repos/SketchedDoughnut/development/releases/latest' # link format: https://api.github.com/repos/{owner}/{repo}/releases/latest
    dest = "https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest"
    try:
        response = requests.get(dest)
    except:
        run_no = threading.Thread(target=lambda:no_confirm(texts_msg = 'Update failed, exiting...', sleep_time = 3), daemon=True)
        run_no.start()
        #time.sleep(2)
        exit()
    # print(response.json()["name"])

    # print
    print('----------------------------')

    # check if version file exists (how to handle if not?)
    if os.path.exists(os.path.join(wDir, 'version.json')):
        print('File found: Comparing versions...')

        temp = str(response.json()["body"])
        temp_list = temp.split()
        new_version = temp_list[0]
        directory = temp_list[1]
        status = temp_list[2]

        # loads version
        f = open(f'{wDir}/version.json', 'r')
        current_version = json.load(f)
        f.close()

        # seeing if there is a difference
        if str(current_version) != new_version:


            # new addition- run check modes for multiple updates
            print('Name decrepancy: Analyzing modes...')
            import eggs as egg
            current_mode, new_mode, status, ran = egg.eval_modes(current_version)
            print('----------------------------')
            directory = new_mode


            if ran:
                print(f"""It appears you are multiple updates behind.
Affected areas: {directory},
Status: {status}
Prompting for update...""")
                
            elif not ran:
                print(f"""Name decrepancy: {current_version} != {new_version} 
Affected areas: {directory} 
Status: {status} 
Prompting for update...""")
            global WIDTH
            global HEIGHT
            do_exit = True
            confirm = False
            #pygame.init()
            WIDTH = pygame.display.Info().current_w
            HEIGHT = pygame.display.Info().current_h
            text_msg = 'Do you want to update?'
            text_height = (HEIGHT / 4)
            _cancel = True


        elif str(current_version) == new_version:
            print('No decrepancy: exiting...')
            text_msg = 'No updates found.'
            f = open(f'{wDir}/state.json', 'w')
            json.dump(False, f)
            f.close()
            time.sleep(0.5)
            do_exit = True
            confirm = True

# the buttons it draws (yes or no)
def buttons(yes_list, no_list):
    yes_zone = pygame.Rect(yes_list[0], yes_list[1], yes_list[2], yes_list[3])
    no_zone = pygame.Rect(no_list[0], no_list[1], no_list[2], no_list[3])
    return [[GREEN, yes_zone], [RED, no_zone]]

def exit_handler(mode=False):
    global do_exit, confirm, _cancel, text_height
    text_msg = 'Exiting...'
    if not mode:
        time.sleep(3)
        do_exit = True
        confirm = True

def yes_confirm():
    global do_exit, confirm, text_msg, text_height, _cancel, update_exit
    print('Update comfirmed. Initializing...')
    # objective is to reach back up to data.json and change update and bounds
    _cancel = False
    text_msg = 'Reaching...'
    text_height = (HEIGHT / 2)
    time.sleep(0.25)
    # god long file path
    main_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    #print(main_path) ##################
    data_path = os.path.join(main_path, 'setup/data.json')
    #print(data_path) ##################################
    f = open(data_path, 'r')
    temp_dict = json.load(f)
    f.close()
    temp_dict['update'] = True
    temp_dict['bounds'] = directory
    f = open(data_path, 'w')
    json.dump(temp_dict, f)
    f.close()
    text_msg = 'Pushed to data.json'
    time.sleep(0.25)
    text_msg = 'Updating state...'
    time.sleep(0.25)
    f = open(f'{wDir}/state.json', 'w')
    json.dump(True, f)
    f.close()
    text_msg = 'Please relaunch.'
    print('Update setup finished')
    time.sleep(1.5)
    exit_handler()

    pass

def no_confirm(texts_msg: str = 'Cancelling...', sleep_time: int = 0.75):
    global _cancel, do_exit, confirm, text_height, text_msg
    text_msg = texts_msg
    _cancel = False
    text_height = (HEIGHT / 2)
    time.sleep(sleep_time)
    do_exit = True
    confirm = True
################################################################################################

# not depreciated anymore :D
# print('----------------------------')
# print('NOTE: THIS UPDATE AGENT IS CURRENTLY DEPRECIATED. WHY? I AM LAZY.')

# button data
width = (250)
height = (HEIGHT / 15)
x = (WIDTH / 2) - (width / 2)
y = 2 * (HEIGHT / 4)
yes = [x, y, width, height] # green
y = 3 * (HEIGHT / 4)
no = [x, y, width, height] # red
objects = buttons(yes, no)
yes_zone = objects[0][1]
no_zone = objects[1][1]

#text
text_height = (HEIGHT / 2)
# thread objects
check = threading.Thread(target=lambda:check_version(), daemon=True)
exit_thread = threading.Thread(target=lambda:exit_handler())

# start threads
check.start()

while True:
    do_exit = False
    confirm = False
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("thing!")

    while not do_exit:
        pygame.time.delay(1)

        # if close window, prompt for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if not exit_thread.is_alive:
                    exit_thread.start()

        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        window.fill(BLACK)
        font = pygame.font.Font('freesansbold.ttf', round(24))
        text = font.render(text_msg, True, WHITE, None) # text, some bool(?), text color, bg color
        text_rect = text.get_rect(center=(WIDTH / 2, text_height))
        window.blit(text, text_rect)

        if _cancel:
            yes = pygame.draw.rect(window, objects[0][0], (yes_zone))
            no = pygame.draw.rect(window, objects[1][0], (no_zone))
            if yes.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    try:
                        run_no.join()
                    except:
                        pass
                    run_yes = threading.Thread(target=lambda:yes_confirm(), daemon=True)
                    run_yes.start()
            if no.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    try:
                        run_yes.join()
                    except:
                        pass
                    run_no = threading.Thread(target=lambda:no_confirm(), daemon=True)
                    run_no.start()

        pygame.display.update()

    pygame.quit()
    if confirm:
        break
