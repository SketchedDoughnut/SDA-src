# builtins
import os
import shutil
import json
import time
import sys

# packages
import requests

# file imports
from .tools import backup as b
from .tools import download as d
from .tools import extract as ee
from .tools import copy as c
from .tools import verify as v

def createShortcut(path, target='', wDir='', icon=''):  
    from win32com.client import Dispatch
    ext = path[-3:]
    if ext == 'url':
        #shortcut = file(path, 'w')
        shortcut = open(path, 'w')
        shortcut.write('[InternetShortcut]\n')
        shortcut.write('URL=%s' % target)
        shortcut.close()
    else:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wDir
        if icon == '':
            pass
        else:
            shortcut.IconLocation = icon
        shortcut.save()


def update_handler_setup(
        setup_wDir,
        everything_path,
        mode
    ):

    '''
    flow for full re-install
    
        - deletes previous tmp folder in setup
        - creates new tmp folder
        - alerts that this installation requires user interaction
        - download .zip
        - extract .zip
        - copy "full-redo" into the directory ABOVE of main
        - get rid of tmp
        - reset data.json
        - provide further instructions on what to do
        done!
    '''

    # setup the vars provided here
    # commit label
    #release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
    release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest")
    release_version = release_version.json()
    release_version = str(release_version['body'])
    release_version = release_version.split()
    release_version = release_version[0]

    # other vars
    ut2_wDir = os.path.dirname(os.path.dirname(os.path.dirname(setup_wDir)))
    zip_download_path = f"{setup_wDir}/tmp/latest_release.zip"
    ext_download_path = f"{setup_wDir}/tmp"
    copy_source = f"{ext_download_path}/SketchedDoughnut-development-{release_version}/everything/full-redo"
    #repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
    repo_url = "https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest"
    dump_location = f'{ut2_wDir}/full-redo'

    
    if mode == 'full-setup':
        # FOR PYTHON
        print(ut2_wDir)

        # FOR COMPILE
        #os.path.dirname(ut2_wDir)

        # cancel if they want to
        print('---------------')
        print('Update: installing full')
        print('- This is a update that requires a re-installation of all game files.')
        print('  Nothing will be saved.')
        print('If you want to backup your files, copy the ENTIRE directory now.')
        print(f'The directory is: {ut2_wDir}/everything')
        if input('Continue? (y/n) ').lower() != 'y':
            print('---------------')
            print('Cancelling...')
            print('Update: Resetting data.json...')
            f = open(f'{setup_wDir}/data.json', 'r')
            td = json.load(f)
            f.close()
            td['bounds'] = 'x'
            td['update'] = False
            td['shortcut'] = True
            f = open(f'{setup_wDir}/data.json', 'w')
            json.dump(td, f)
            f.close()
            input('Enter anything to exit: ')
            sys.exit()

        # clean tmp
        print('---------------')
        print('Update: Cleaning tmp...')
        try:
            shutil.rmtree(f'{setup_wDir}/tmp')
        except:
            print('Update: No prior tmp')

        # make tmp
        print('Update: Making tmp...')
        os.mkdir(f'{setup_wDir}/tmp')
        
        # delete previous full-redo
        print('Update: Cleaning full-redo...')
        try:
            shutil.rmtree(f'{ut2_wDir}/full-redo')
        except:
            print('Update: No prior full-redo')

        # download .zip
        print('Update: Downloading .zip...')
        d.download_latest_release(repo_url, zip_download_path)

        # extract files
        # https://www.geeksforgeeks.org/unzipping-files-in-python/
        print('Update: Extracting files...')
        time.sleep(1)
        ee.extract(zip_download_path, ext_download_path)
        
        # get commit label (teehee)
        print('Update: Getting commit label...')
        time.sleep(0.5)

        # copy full-redo folder ABOVE current installation main, so it is:
        # root: main, full-redo (in same dir)

        # copy files to new directory
        # https://pynative.com/python-copy-files-and-directories/
        print('Update: Copying control folder...')
        print(f'Update: Copying files to {dump_location}')
        c.copy(copy_source, dump_location)

        # transfer shortcut - src: fiesta.py
        print('Update: Redirecting shortcut...')
        import winshell
        desktop = winshell.desktop()     
        path = os.path.join(desktop, "game_name.lnk") # CHANGE game_name TO NAME
        target = f"{ut2_wDir}/full-redo/full-redo.exe" # CHANGE TO EXE
        wDir = f"{ut2_wDir}/full-redo"
        icon = f"{ut2_wDir}/full-redo/full-redo.exe" # CHANGE TO EXE
        transShortcut = False
        try:
            createShortcut(target=target, path=path, wDir=wDir, icon=icon)
            transShortcut = True
        except Exception as e:  
            print(f'Update: Shortcut transfer error: {e}')
            transShortcut = False

        # clean up tmp
        print('Update: Cleaning up tmp...')
        try:
            shutil.rmtree(f'{setup_wDir}/tmp')
        except:
            print('Update: No tmp')

        # check install path
        print('Update: Checking install path...')
        if os.path.exists(f'{ut2_wDir}/full-redo'):
            pass
        else:
            print('!!! UPDATE ERROR: The installed directory does not exist. Cancelling.')
            input('Enter anything to exit: ')
            sys.exit()

        # start second part of update
        print('---------------')
        if not transShortcut:
            print(f"""Update: Part 1/2 of update is done.
This installer is incapable of finishing this update, as it will require deleting itself. 
In order to finish this install, please go to --
> {ut2_wDir}/full-redo/
-- and run the file named "full-redo.exe". It will run you through the process to finish this update.""")
            print('---------------')
            input('Enter anything to exit: ')
            sys.exit()

        elif transShortcut:
            print('---------------')
            print('Update: Part 1/2 is done. Please relaunch via the shortcut on your desktop.')
            print('---------------')
            input('Enter anything to exit: ')
            sys.exit()