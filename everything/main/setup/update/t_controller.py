import os
import shutil
import json
import time
import sys

# packages
import requests
 
# file imports
from .tools import backup as b
from .tools import rollback as r
from .tools import download as d
from .tools import extract as ee
from .tools import copy as c
from .tools import verify as v



def update_handler(main_wDir, setup_wDir):

    # setup the vars provided here
    # commit label
    #release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
    release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest")
    release_version = release_version.json()
    release_version = str(release_version['body'])
    release_version = release_version.split()
    release_version = release_version[0]

    # other vars
    mode = 'top'
    zip_download_path = f"{setup_wDir}/tmp/latest_release.zip"
    ext_download_path = f"{setup_wDir}/tmp"
    copy_location = f'{main_wDir}/top'
    json_path = os.path.join(setup_wDir, 'file_list.json')
    everything_path = os.path.dirname(main_wDir)
    #repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
    repo_url = "https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest"
    copy_source = f"{ext_download_path}/SketchedDoughnut-SDA-src-{release_version}/everything/main/top"
    state = False



    if mode == 'top':
        print('---------------')
        print('Update: installing top')
        print('If you want to backup your top, copy the directory now.')
        print(f'The directory is: {main_wDir}/top')
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

        print('---------------')
        print('Update: Cleaning tmp...')
        try:
            shutil.rmtree(f'{setup_wDir}/tmp')
        except:
            print('Update: No prior tmp')
        print('Update: Making tmp...')
        os.mkdir(f'{setup_wDir}/tmp')

        try:
            b.backup_handler(
                main_wDir = main_wDir,
                setup_wDir = setup_wDir,
                backOrLoad = 'back',
                target = 'top'
            )
        except Exception as e:
            print('Update: Backup error:', e)
        
        print('Update: deleting previous top...')
        try:
            shutil.rmtree(f"{main_wDir}/top")
        except Exception as e:
            print('Update: No prior top:', e)
        
        print('Update: Downloading .zip...')
        d.download_latest_release(repo_url, zip_download_path)

        print('Update: Extracting files...')
        # https://www.geeksforgeeks.org/unzipping-files-in-python/
        ee.extract(zip_download_path, ext_download_path)

        print('Update: Getting commit label...')

        print(f'Update: Copying files to {copy_location}...')
        # https://pynative.com/python-copy-files-and-directories/
        c.copy(copy_source, copy_location)

        print('Update: Checking install path...')
        if os.path.exists(copy_location):
            print('Update: Path exists')
        else:
            print('!!! UPDATE ERROR: The installed directory does not exist. Reverting update to backup.')
            print(f'!!! UPDATE ERROR: Path: {copy_location}')
            input('Enter anything to exit: ')
            sys.exit()

        print('Update: Checking file integrity...')
        results = v.verify_files(json_path, everything_path)
        if results:
            b.backup_handler(
                main_wDir = main_wDir,
                setup_wDir = setup_wDir,
                backOrLoad = 'load',
                target = 'top'
            )
            r.decide(False)
            sys.exit()

        print('Update: Cleaning up tmp...')
        try:
            shutil.rmtree(f'{setup_wDir}/tmp')
        except:
            print('Update: No tmp')
        
        print('Update: Resetting data.json...')
        print('Update: Path:', f'{setup_wDir}/data.json')
        f = open(f'{setup_wDir}/data.json', 'r')
        td = json.load(f)
        f.close()
        td['bounds'] = 'x'
        td['update'] = False
        td['shortcut'] = True
        f = open(f'{setup_wDir}/data.json', 'w')
        json.dump(td, f)
        f.close()

        time.sleep(1)
        print('Update: Reaching to version.json...')
        print(f'Update: Path: {main_wDir}/top/container/version.json')
        f = open(f'{main_wDir}/top/container/version.json', 'w')
        print('Update: Dumping version...')
        json.dump(release_version, f)
        f.close()

        time.sleep(0.25)
        print('Update: Reaching to state.json...')
        print(f'Update: Path: {main_wDir}/top/container/version.json')
        f = open(f'{main_wDir}/top/container/state.json', 'w')
        print('Update: Dumping state...')
        json.dump(state, f)
        f.close()

        print('Update: top update complete!')
        print('---------------')
        input('Enter anything to exit: ')
        sys.exit()