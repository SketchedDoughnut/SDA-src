import shutil
import os
import json
import time
import pip

in_folder = False
#################################################################

temp_main_wDir = os.path.dirname(os.path.abspath(__file__))
temp_setup_wDir = os.path.join(temp_main_wDir, 'setup')
if os.path.exists(temp_setup_wDir):
    in_folder = True

if in_folder:
    print('---------------')
    print('It appears this file is in a setup folder. Defaulting to those paths.')
    setup_wDir = temp_setup_wDir
    main_wDir = temp_main_wDir

elif not in_folder:
    print('---------------')
    print('It appears this file is not within a setup folder. Defaulting to those paths.')
    main_wDir = temp_main_wDir
    setup_wDir = main_wDir


# for run 
rules = open(os.path.join(main_wDir, 'config.json'), 'r')

rules = json.load(rules)

# for run
if rules['env'] == 'run':
    temp = open(os.path.join(setup_wDir, 'data.json'), 'r')

delete_path = json.load(temp)
delete_path = delete_path["remove_path"]
temp.close()
print('---------------')
print(f'Delete: Un-installing game from the following directory: {delete_path}')
if input('Continue? (y/n) ').lower() == 'n':
    print('Cancelling...')
    time.sleep(5)
    exit()

time.sleep(0.025)

# get path from delete.json
print('Delete: Acquiring JSON path...')
time.sleep(0.025)

# for run
if rules['env'] == 'run':
    read_file = open(f'{setup_wDir}/data.json', 'r')

path = json.load(read_file)
del_path = path["remove_path"]
shrt_path = path['abs_shortcut']

if ('game_name' in del_path) == False:
    print(f'No game name found ({del_path}). exiting in 5s...')
    time.sleep(5)
    exit()

read_file.close()
print(f'Delete: Directory path: {del_path}/')
print(f'Delete: Shortcut path: {shrt_path}')
time.sleep(0.025)

# deleting folder
print('Delete: deleting directory...')
try:
    shutil.rmtree(del_path)
    print('Delete: Directory gone.')

except Exception as e:
    print(f'Delete: Directory error: {e}')

time.sleep(0.05)

print('Delete: Deleting shortcut...')
time.sleep(0.025)

try:
    os.remove(shrt_path)
    print('Delete: Shortcut gone.')
    time.sleep(0.025)

except Exception as e:
    print(f'Delete: Shortcut error: {e}')

print('Delete: Clearing data...')
time.sleep(0.025)

# for run
if rules['env'] == 'run':
    write_file = open(f'{setup_wDir}/data.json', 'w')

path["remove_path"] = ""
path["abs_shortcut"] = ""
json.dump(path, write_file)
write_file.close()
exit()