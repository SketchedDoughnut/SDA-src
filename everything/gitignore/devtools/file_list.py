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
direct_filter = [
    '__pycache__'
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

for string in file_list:
    # print(string)
    for filtered in direct_filter:
        if filtered in string:
            file_list.remove(string)

f = open(r'everything\main\setup\file_list.json', 'w')
json.dump(file_list, f)
f.close()
print('Dumped.')