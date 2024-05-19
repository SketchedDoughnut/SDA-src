# loading 
import os
import json
import time
import pygame

def load_map():
    # establish wDir
    wDir = os.path.dirname(os.path.abspath(__file__))
    # end current session
    for _ in range(3):
        print('----------------------')
    print('Exiting current session...')
    pygame.quit()
    print('----------------------')
    print('Please put your map file (.json) into the following directory:')
    print(f'- {wDir}/maps_in/')
    input('Enter anything to continue: ')
    while True:
        print('----------------------')
        print('Input the name of your map. Ex: my_map:')
        map_name = input('-> ')
        print('----------------------')
        print('Assembling path of map...')
        map_path = f'{wDir}/maps_in/{map_name}.json'
        print('----------------------')
        print('The path is:', map_path)
        if input('If this is right, enter y. otherwise, enter anything else to redo this\n-> ').lower() == 'y':
            break
    print('Returning path...')
    return map_path