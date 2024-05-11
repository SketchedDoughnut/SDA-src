'''
The goal of this file is to be used as a temporary file, positioned above main,
that will re-install ALL files. This is if fiesta.exe needs an update.
'''

# import builtin
import os
import shutil
import time
import json

# import installed
import requests

# SHIT WE DONT HAVE THE OTHER FILES RAHHHHHHH

print('Welcome to part 2/2 of the update.')
print('The update will continue when you authorize it.')
input('Enter anything to continue: ')
print('---------------')
'''
flow

    - establish all variables and paths
    - clean up any previous tmp (redundancy)
    - delete previous game_name
    - download
    - extract (in same dir, /tmp)
    - copy "game_name" and put it where the previous one was
'''

print('Update: Setting up variables...')

#############################################################################
#############################################################################
#############################################################################

# FOR PYTHON
# wDir, folder above this (full-redo)
wDir = os.path.dirname(os.path.abspath(__file__))
 # a directory above full-redo
high_wDir = os.path.dirname(wDir)

# FOR COMPILE
# wDir, folder above this (full-redo)
wDir = os.path.dirname(wDir) ############### darn vscode
high_wDir = os.path.dirname(high_wDir) # changed from wDir to high_wDir ############### darn vscode

# commit label, the random crap (in this case we ignore the bounds since we know we are installing full)
#commit_label = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
commit_label = requests.get("https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest")
commit_label = commit_label.json()
commit_label = str(commit_label['body'])
commit_label = commit_label.split()
commit_label = commit_label[0]

# url for install
#repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
repo_url = "https://api.github.com/repos/SketchedDoughnut/SDA-src/releases/latest"

# tmp directory
tmp_path = f'{wDir}/tmp' # changed from wDir to high_wDir

# zip directory for install
zip_path = f'{tmp_path}/latest-release.zip'

# extract path for install
extract_path = f"{tmp_path}/SketchedDoughnut-SDA-src-{commit_label}/everything"

# everything path
everything_path = f'{high_wDir}/everything'
eb1 = os.path.dirname(everything_path)

# copy paths (source, destination) for install
copy_source = zip_path
copy_destination = everything_path

# edit path
# variable to edit the data.json of the installed installer to: "shortcut": true
# edit setup installer file

esif = f'{everything_path}/main/setup/data.json' # added main
vsif = f'{everything_path}/main/top/container/version.json' # added main

print(f"""---------------
Variables:
    - wDir: {wDir}
    - high_wDir: {high_wDir}
    - commit_label: {commit_label}
    - repo url: None
    - tmp_path: {tmp_path}
    - zip_path: {zip_path}
    - extract_path: {extract_path}
    - everything_path: {everything_path}
    - eb1: {eb1}
    - copy_source: {copy_source}
    - copy_destination: {copy_destination}
    - esif: {esif}
    - vsif: {vsif}
""")
#############################################################################
#############################################################################
#############################################################################

import update.fr_controller_install as frc
frc.update_handler_install(
    mode = 'full-install',
    tmp_path = tmp_path,
    zip_path = zip_path,
    everything_path = everything_path,
    extract_path = extract_path,
    repo_url = repo_url,
    commit_label = commit_label,
    esif = esif,
    vsif = vsif
)