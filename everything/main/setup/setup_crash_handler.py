# this file is a template to paste into all other crash handlers
# all code goes inside try and except, besides this
# except invokes crash handler
# the crash handler is only meant to be used inside of everything/
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

        










class Crash_handler:
    def __init__(self, wDir: str = 'will autofill', error: str = 'error', mode: str = 'run'):
        wDir = os.path.dirname(os.path.abspath(__file__))
        self.path_tools = Path_tools()
        self.error = error
        if mode == 'run':
            print('------------------')
            print('Crash Handler setting up...')
            self.current_time = self.get_time()
            print('Acquired time...')
            forward_slash_path = self.path_tools.convert_path(wDir, '/')
            logged_path = self.log_data(forward_slash_path)
            print('Data acquired, dumped...')
            print('------------------')
            print('Crash documented to:', f'{logged_path}')
            print('------------------')
            input('Enter anything to exit: ')
            exit()
        elif mode == 'setup':
            pass
        else:
            print('Invalid crash handler initialization.')
            import sys
            sys.exit()

    def get_time(self) -> str: # copied over from old crash handler, idek what it does
        import time
        s = (time.ctime(time.time()))
        s = s.replace(':', '-')
        s = s.split()
        for __ in range(2):
            s.pop(0)
        n_string = ''
        for num in s:
            n_string += num
            if s.index(num) != len(s) -1:
                n_string += '_'
        return n_string
    
    def log_data(self, path: str, do_log: bool = True) -> str:
        everything_path_list = self.path_tools.promote_path(path)
        everything_path = everything_path_list[1]
        log_path = everything_path + 'crash/dumps'
        timed_path = log_path + f'/crash_log_{self.current_time}.log'
        backslash_timed_path = self.path_tools.convert_path(timed_path, '\\')
        if do_log:
            f = open(backslash_timed_path, mode='w')
            f.write(self.error)
            f.close()
        return backslash_timed_path