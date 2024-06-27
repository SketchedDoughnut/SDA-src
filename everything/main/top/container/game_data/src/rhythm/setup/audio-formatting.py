import time
import os
import pygame
from pygame.locals import *
import json

f = open("everything\\main\\top\\container\\game_data\\src\\rhythm\\setup\\count\\count.json", 'r')
num = json.load(f)
f.close()
 
pygame.init()
WIDTH = 1000
HEIGHT = 1000

##################################################

start = time.time()
end = 0

space = False
time_list = [['end', 'start', 'dif']]
print('-----------------------------------------')
goal = input('file name (.json): '), num
if goal[0] == 'length':
    path =input('-> ')
    f = open(path, 'r')
    length = len(f.read())
    f.close()
    print(length)
    exit()

print('Proceed, S to start.')
print('-----------------------------------------')

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("thing!")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_s]:
        running = True
        break

# https://www.geeksforgeeks.org/python-playing-audio-file-in-pygame/
m = pygame.mixer
m.init()

# https://open.spotify.com/track/6FEisGZPcJyGwSpuhH1fMx?si=f23f1eb11c6349dd
m.music.load('everything/main/top/container/game_data/src/rhythm/songs_ogg/boggle.ogg')

# https://open.spotify.com/track/4RvWPyQ5RL0ao9LPZeSouE?si=37529cd0288c4cf8
#m.music.load('everything/main/top/container/game_data/src/rhythm/songs_ogg/rule_the_world.ogg)

# https://open.spotify.com/track/75eo472nc6DIqpwlVOA91B?si=77a2e07864e5445a
#m.music.load('main\\top\game_data\src\\rhythm\songs_ogg\\rush.ogg')

# https://open.spotify.com/track/4Po97bPnn3ISdEkuJBMt2f?si=6a51325cff4a49e2
#m.music.load('main\\top\game_data\src\\rhythm\songs_ogg\stayed_gone.ogg')


m.music.set_volume(0.75)
m.music.play()

def dump():
    global running
    global num
    print('dumping...')
    f = open(f'everything/main/top/container/game_data/src/rhythm/setup/audio-out/{goal}.json', 'w')
    json.dump(time_list, f)
    f.close()

    print(f'iterating num... ({num} -> {num + 1})')
    num += 1
    f = open(f'everything\\main\\top\container\game_data\src\\rhythm\setup\count\count.json', 'w')
    json.dump(num, f)
    f.close()
    
    print('Done. Exiting')
    running = False

while running:
    # delay
    pygame.time.delay(int(0.001 * 1000))

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # gathering input data
    keys = pygame.key.get_pressed()

    if keys[K_x]:
        dump()
        
        print('Done. Exiting')
        running = False

    if keys[K_SPACE]:
        if space == False:
            end = (time.time())
            dif = (end - start)
            start = end
            #time_list.append([end, start, dif])
            time_list.append([dif, True])
            space = True
            print(f"""
start: {start}
end: {end}
dif: {dif}""")
            
    elif not keys[K_SPACE]:
        space = False
        # time_list.append([0.001, False])
        # print('added default')

    # exits
    if keys[K_LCTRL]:
        if keys[K_c]:
            running = False
        elif keys[K_w]:
            running = False
    if keys[K_ESCAPE]:
        running = False

    if m.music.get_busy() == False:
        dump()
        
    pygame.display.update()