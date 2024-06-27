# This file lists every existing file in everything
# It is used to verify after an update is installed
########################################################################
import os
import shutil
import time
import json

file_list = []
blacklist = [
    'everything\\main\\top\\container\\game_data\\src\\rhythm\\setup'
]

def iter(path):
    files = []
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if f not in blacklist:
            if os.path.isdir(f):
                files.extend(iter(f))
            elif os.path.isfile(f):
                files.append(f)
    return files


file_list = iter('everything')
print('Indexed.')

f = open('everything\main\setup\file_list.json', 'w')
json.dump(file_list, f)
f.close()
print('Dumped.')