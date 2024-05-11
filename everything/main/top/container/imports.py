# install files necessary with pip
print('Installing pip files...')
print('----------------------------')
import pip

# also consider cryptography, pywin32 
pip.main(['install', 'pygame', 'requests', 'pywin32', 'winshell'])

# test every other import. Why? God knows why, man.
# builtins
print('----------------------------')
print('Testing bulitins...')
import timeit
import time
import shutil
import json
import os 
import threading
import random

# installed
print('Testing installed...')
import pygame
from pygame.locals import *
import requests
import winshell