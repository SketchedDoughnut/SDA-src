import shutil
import os
import json

def decide(
    if_full_redo
    ):
    if if_full_redo:
        print('------------------------------------')
        print('Your installation is improper due to a developer issue. Please report this issue back to the developers.')
        print('The update will cancel and your game will act as normal.')
        print('------------------------------------')
        input('Enter anything to proceed: ')