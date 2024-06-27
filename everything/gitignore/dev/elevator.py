# this file is a template to be pasted into all other elevators
# it is meant to be used inside of everything/
# It uses a similar system for promoting paths as the crash handler
########################################################################
import os

class Path_tools:
    def __init__(self) -> None:
        pass

    def convert_path(self, path: str, mode: str) -> str: # copied over from old crash handler, idek what it does
        n_string = ''
        for letter in path:
            if mode == '/':
                if letter == '\\':
                    n_string += '/'
                else:
                    n_string += letter
            elif mode == '\\':
                if letter == '/':
                    n_string += '\\'
                else:
                    n_string += letter
        return n_string

    def promote_path(self, path: str) -> list[list, str]: # promotes path until it reaches everything/
        forward_slash_path = self.convert_path(path, '/') # convert to forward slash path, regardless of input
        path_list = [] 
        carry_over = ''
        new_path = ''
        for letter in forward_slash_path: # go over every letter, and make a list of each argument: (folder1), (folder2), etc
            if letter == '/':
                path_list.append(carry_over)
                carry_over = ''
                continue
            carry_over += letter
        path_list.append(carry_over)
        while path_list[-1] != 'everything': # remove things from the end until we reach everything
            path_list.pop()
        for folder in path_list: # create a new path
            new_path += folder
            new_path += '/'
        new_path.removesuffix('/')
        return [path_list, new_path]

        










class Elevatorr:
    def __init__(self):
        self.raw_wDir = os.path.dirname(os.path.abspath(__file__))
        self.path_tools = Path_tools()
        self.wDir = self.path_tools.convert_path(self.raw_wDir, '/')
        self.elevated_universe = self.elevate_path(self.wDir)

    def elevate_path(self, path) -> str:
        elevated_list = self.path_tools.promote_path(path)
        elevated: str = elevated_list[1]
        elevated = elevated.removesuffix('/')
        elevated = os.path.dirname(elevated)
        elevated += '/universe'
        return elevated
    
Elevator = Elevatorr()