import shutil
import time
import os
import json
import requests

'''
flow
    - when invoked, an update has failed
    - load files from backup file (given mode top or game_data)
    - put them in respective locations
    - return an error message about potentially damaged files (offer full-redo re-install)
        - if yes, do full-redo
        - if no, warn them again but reset data.json
'''

# this function is invoked:
#   - BEFORE A DELETION OF THE DIRECTORY BEING UPDATED IS DONE, 
#   - IF AN UPDATE FAILS, 
#   - AFTERWARDS FOR CLEANUP 
#       - (MUST BE AUTHORIZED, GIVE THEM A CHOICE TO SAVE)

def backup_handler(
        main_wDir, 
        backOrLoad, 
        target
    ):

    # if full-redo
    if target == 'full-redo':
        # set up vars
        copy_source = os.path.dirname(main_wDir)
        top_wDir = os.path.dirname(copy_source)
        copy_destination = f'{top_wDir}/full-redo/update/tools/backups/everything'

        if backOrLoad == 'back':
            print('Update: Deleting previous backup...')
            print('    - location:', copy_destination)
            input('--> Enter anything to authorize deletion: ')
            try:
                shutil.rmtree(copy_destination)
                print('Update: Previous backup deleted')
            except:
                print('Update: No prior backup')
            print('Update: Backing up everything...')
            print('    - source:', copy_source)
            print('    - destination:', copy_destination)
            shutil.copytree(copy_source, copy_destination)
            print('Update: Files are backed up')

        elif backOrLoad == 'load':
            print('Update: Cleaning failed installation...')
            shutil.rmtree(copy_source)
            print('Update: Reloading backup of everything...')
            shutil.copytree(copy_destination, copy_source)

    else:
        print('No valid target.')
        exit()