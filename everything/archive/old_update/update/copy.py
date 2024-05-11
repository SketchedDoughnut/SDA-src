import shutil
import os

def copy(source_dir, destination_dir, mode='folder'):
    if mode == 'folder':
        shutil.copytree(source_dir, destination_dir)
    if mode == 'file':
        shutil.copyfile(source_dir, destination_dir)