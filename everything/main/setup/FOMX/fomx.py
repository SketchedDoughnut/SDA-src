'''
PLEASE REFER TO ./GUIDE.TXT FOR MORE INFO
~ swoosh ~
'''

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
########################################################################
try:   
    # builtins
    import os 
    import shutil
    import time
    import json
    import sys
    
    # external
    import requests
    
    # file imports
    import tools.download as download
    import tools.extract as extract
    
    # ---------------------------------------------
    url = 'https://api.github.com/repos/SketchedDoughnut/SDA-FOMX/releases/latest'
    wDir = os.path.dirname(os.path.abspath(__file__))
    above_everything_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(wDir))))
    
    def load_current_label(dir: str) -> str:
        path = os.path.join(dir, 'version.json')
        f = open(path, 'r')
        current = str(json.load(f))
        f.close()
        return current
    
    def get_release_info(local_url: str) -> list:
        data = requests.get(local_url).json()
        data = str(data['body'])
        data = data.split()
        id = data[0]
        data.remove(id)
        n_word = ''
        for word in data: # re-assemble words with one-spacing
            n_word += word
            n_word += " "
        return [id, n_word]
    
    
    current_label = load_current_label(wDir)
    latest_label, content = get_release_info(url)
    print('---------------')
    print('FOMX: DATA')
    print('    - current commit label:', current_label)
    print('    - commit label of newest release:', latest_label)
    print('FOMX: comparing versions...')
    if current_label != latest_label:
        print('FOMX: versions do not match.')
        print('---------------')
        if input('FOMX: do you want to see the info for this update? (y/n): ').lower() == 'y':
            print('---------------')
            print('Info:')
            print('-', content)
            print('---------------')
        else:
            print('FOMX: skipping...')
            print('---------------')
        if input('Download this update? This is highly recommended (y/n): ').lower() == 'y':
            pass
        else:
            print('---------------')
            print('FOMX: exiting...')
            time.sleep(1)
            sys.exit()
    
    else:
        print('FOMX: versions match. Continuing to launch')
        time.sleep(0.5)
        sys.exit()
        
    print('---------------')
    # vars
    tmp_path = os.path.join(wDir, 'tmp')
    zip_path = f'{tmp_path}/latest_release.zip'
    copy_location = f'{tmp_path}/SketchedDoughnut-SDA-FOMX-{latest_label}/data'
    bounds_json = f'{copy_location}/bounds.json'
    
    
    
    print('FOMX: attempting to delete previous tmp...')
    try:
        shutil.rmtree(tmp_path)
        print('FOMX: previous tmp deleted')
    except:
        pass
    os.mkdir(tmp_path)
    
    print('FOMX: downloading .zip...')
    download.download_latest_release(url, zip_path)
    time.sleep(0.5)
    
    print('FOMX: extracting...')
    extract.extract(zip_path, tmp_path)
    
    print('FOMX: reading bounds file...')
    f = open(bounds_json, 'r')
    bounds = json.load(f)
    f.close()
    time.sleep(0.5)
    
    print('FOMX: bounds description:')
    print('-', bounds['description'])
    print('FOMX: files affected:')
    print('-', bounds['file_details'])
    
    print('FOMX: formatting data list...')
    n_list = []
    for path, file in zip(bounds['file_paths'], bounds['file_details']):
        n_list.append([file[1], os.path.join(copy_location, file[0]), os.path.join(os.path.join(above_everything_dir, path), file[0]), file[0]])
    
    print('---------------')
    print('FOMX: verifying files exist...')
    for data in n_list:
        print('- verifying:', data)
        if not os.path.exists(data[1]): # if destination exists
            print('-- source does not exist.')
            exit()
        # if not os.path.exists(data[2]): # if copy file exists
        #     print('-- dest does not exist.')
        #     exit() 
    print('FOMX: all files exist.')
    print('---------------')
    
    print('FOMX: Copying over code...')
    time.sleep(0.5)
    for file in n_list:
        # set vars
        mode = file[0]
        source = file[1]
        dest = file[2]
        if mode == 'normal' or mode == 'json':
            op = 'r'
            wr = 'w'
        elif mode == 'binary':
            op = 'rb'
            wr = 'wb'
    
        # r/w for anything besides json
        if mode != 'json':
            f = open(source, op)
            content = f.read()
            f.close()
            f = open(dest, wr)
            f.write(content)
            f.close()
            print(f'- wrote content from "{source}" to "{dest}"')
        # r/w for json
        elif mode == 'json':
            f = open(source, op)
            content = json.load(f)
            f.close()
            f = open(dest, wr)
            json.dump(content, f)
            f.close()
            print(f'- wrote content from "{source}" to "{dest}"')
        
    
    
    print('---------------')
    print('FOMX: cleaning up tmp...')
    time.sleep(0.25)
    shutil.rmtree(tmp_path)
    
    print('FOMX: updating local version...')
    f = open(os.path.join(wDir, 'version.json'), 'w')
    json.dump(latest_label, f)
    f.close()
    time.sleep(0.25)
    
    print('---------------')
    print('FOMX process is done, Enter anything to continue on to launch: ')
    input('--> ')
    sys.exit()


except Exception as e:
    import os
    import traceback
    Crash_Handler(
        wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        error = traceback.format_exc()
    )
