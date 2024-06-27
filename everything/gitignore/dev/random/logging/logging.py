class Crash_Handler:
    def __init__(self, wDir, error):
        print('------------------')
        print('Crash Handler setting up...')
        con = self.convert_path(wDir, '/')
        con = self.split_path(con)
        con = self.assemble_path(con)
        con = self.promote_path(con)
        print('Path formatted...')
        dumps_path = self.assemble_dir(con)
        print('Directory assembled...')
        con = self.get_data(dumps_path)
        self.dump_data(con, error)
        print('Data acquired, dumped...')
        print('------------------')
        print('Crash documented to:', f'{con}')
        print('------------------')
        input('Enter anything to exit: ')
        exit()

    def convert_path(self, path, mode):
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
    
    def split_path(self, path):
        n_string = ''
        n_list = []
        for letter in path:
            if letter == '/':
                n_list.append(n_string)
                n_string = ''
            else:
                n_string += letter
        while n_list[0] == " ":
            n_list.pop(0)
        return n_list
    
    def assemble_path(self, path_list):
        n_string = ''
        for word in path_list:
            n_string += word
            n_string += '/'
        return n_string
    
    def remove_n_path_index(self, path):
        path_list = self.split_path(path)
        path_list.pop(len(path_list) - 1)
        path = self.assemble_path(path_list)
        return path_list, path
    
    def promote_path(self, path):
        while True:
            path_list, path = self.remove_n_path_index(path)
            if path_list[len(path_list) - 1] == 'everything':
                break
        return path

    def assemble_dir(self, path):
        path += 'crash/dumps'
        return path
    
    def format_time(self):
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

    def get_data(self, dumps_dir):
        import os
        import json
        time_val = self.format_time()
        nc_log = os.path.join(dumps_dir, f'crash_log_{time_val}.log')
        nc_log = self.convert_path(nc_log, '\\')
        return nc_log

    def dump_data(self, path, error):
        #import json
        f = open(path, 'w')
        #json.dump(error, f)
        f.write(error)
        f.close()






try:
    raise KeyError
except:
    import traceback
    import os
    Crash_Handler(
        wDir = os.path.abspath(__file__),
        error = traceback.format_exc()
    )

# https://stackoverflow.com/questions/56549300/handle-exception-when-running-python-script-from-another-python-script
# https://www.freecodecamp.org/news/python-bytes-to-string-how-to-convert-a-bytestring/