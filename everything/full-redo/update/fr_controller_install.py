# builtins
import os
import shutil
import json
import time

# packages
import requests

# file imports
from .tools import backup as b
from .tools import rollback as r
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


def update_handler_install(
    mode,
    tmp_path,
    zip_path,
    everything_path,
    extract_path,
    other_path,
    folder_paths,
    back_everything,
    repo_url,
    commit_label,
    esif,
    vsif
    ):
    if mode == 'full-install':
        print('---------------')
        print('Update: Deleting previous tmp...')
        try:
            shutil.rmtree(tmp_path)
        except:
            print('Update: No prior tmp')
        print('Update: Creating new tmp...')
        os.mkdir(tmp_path)

        main_wDir = f'{everything_path}/main'
        setup_wDir = f'{everything_path}/main/setup'
        
        try: 
            b.backup_handler(
                main_wDir = main_wDir,
                backOrLoad = 'back',
                target = 'full-redo'
            )
        except Exception as e:
            print('Update: Backup error:', e)
        
        print('Update: Downloading .zip...')
        d.download_latest_release(repo_url, zip_path) # changed tmp_path to zip_path

        print('Update: Extracting files...')
        ee.extract(zip_path, tmp_path)

        print('Update: Deleting previous everything...')
        try:
            shutil.rmtree(everything_path)
        except:
            print('Update: No prior everything')

        print('Update: Copying files...')
        c.copy(extract_path, everything_path)

        # NEW SYSTEM FOR COPYING OVER EXTRA FILES
        print('Update: Copying other files...')
        for file in other_path:
            c.copy(file[0], f'{back_everything}/{file[1]}', mode='file')
            print('- copying:', file[1])

        # new new system for creating universe/ folders if non existent
        print('Update: Creating universe if nonexistent...')
        for folder in folder_paths:
            try:
                os.mkdir(f'{back_everything}/{folder}')
                print('- created:', folder)
            except Exception as e:
                print('- error creating universe folder:', e)

        print('Update: Redirecting shortcut...')
        import winshell
        desktop = winshell.desktop()     
        path = os.path.join(desktop, "game_name.lnk") # CHANGE game_name TO NAME
        target = f"{everything_path}/main/setup/fiesta.exe" # CHANGE TO EXE
        wDir = f"{everything_path}/main/setup"
        icon = f"{everything_path}/main/setup/fiesta.exe" # CHANGE TO EXE
        try:
            createShortcut(target=target, path=path, wDir=wDir, icon=icon)
        except Exception as e:
            print(f'Update: Shortcut transfer error: {e}')

        print('Update: Checking file integrity...')
        json_path = f'{everything_path}/main/setup/file_list.json'
        results = v.verify_files(
            json_path = json_path,
            everything_path = everything_path
        )

        if results:
            b.backup_handler(
                main_wDir = main_wDir,
                backOrLoad = 'load',
                target = 'full-redo'
            )
            r.decide(True)

        print('Update: Reaching into data.json...')
        print('Update: Path:', esif)
        f = open(esif, 'r')
        td = json.load(f)
        f.close()
        td['shortcut'] = True
        td['update'] = False
        td['bounds'] = 'x'
        print('Update: Dumping into data.json...')
        print('Update: Path:', esif)
        f = open(esif, 'w')
        json.dump(td, f)
        f.close()
        print('Update: Reaching into version.json...')
        print('Update: Path:', vsif)
        print('Update: Dumping into version.json...')
        print('Update: Path:', vsif)
        f = open(vsif, 'w')
        json.dump(commit_label, f)
        f.close()
        print('Update: Cleaning up tmp...')
        shutil.rmtree(tmp_path)
        print('Update: Full re-install done!')
        print('---------------')
        print('Update: Please relaunch to use your installation.')
        input('Enter anything to exit: ')
        exit()
