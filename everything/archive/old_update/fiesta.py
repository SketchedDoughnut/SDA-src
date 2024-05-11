# importing builtin
import os
import time
import shutil
import timeit

# downloader imports(?)
import json
import requests
import urllib.request 

'''
{
    "remove_path": "", 
    "abs_shortcut": "", 
    "shortcut": false, 
    "update": false, 
    "bounds": "x"
}
'''
########################################################################
in_folder = False

class Install:

    # init
    def __init__(self, mode=0):
        global in_folder

        # for run
        # setting up all directories
        '''
        path behaviors (why do I have to do this UGH)
        
        - when in a setup folder: FAIL
            - file paths will not go back enough. Instead, main will go back into setup, making it main/setup.
            - setup will add one more setup, making it main/setup/setup.
            - these will not pass the folder requirement and will FALSELY claim that it is not in a folder.

        - when not in a setup folder: WORK
            - file paths do go back enough, making main into main/ (with desktop example, it makes it into desktop).
            - setup (using desktop example), becomes desktop/setup (not used, however, if it is detected properly).

        - so what we want to do:
            - get main path first
            - check for setup in main path (if __ in __)
                - if yes, check if that path exists
                    - if yes, set that path to setup path
                    - rollback one more for main path
            
                - if no, we know it is not in a setup folder
                    - make sure path exists
                        - if yes, set that to main AND setup 
            '''
        
        ####### NEW SYSTEM
        # establish main directory
        temp_main_wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print('initial main', temp_main_wDir)

        # check for setup in main path
        if 'setup' in temp_main_wDir:
            if os.path.exists(temp_main_wDir):
                temp_setup_wDir = temp_main_wDir
                temp_main_wDir = os.path.dirname(temp_main_wDir)

        else:
            if os.path.exists(temp_main_wDir):
                temp_setup_wDir = temp_main_wDir

        # print('new main', temp_main_wDir)
        # print('setup', temp_setup_wDir)

        if os.path.exists(temp_setup_wDir):
            in_folder = True

        if in_folder:
            print('It appears this file is in a setup folder. Defaulting to those paths.')
            # for testing as .py
            #self.setup_wDir = os.path.join(temp_setup_wDir, 'setup')
            self.setup_wDir = temp_setup_wDir
            self.main_wDir = temp_main_wDir
            print(self.main_wDir)
            print(self.setup_wDir)
        
        elif not in_folder:
            print('It appears this file is not within a setup folder. Defaulting to those paths.')
            self.main_wDir = temp_main_wDir
            self.setup_wDir = temp_main_wDir
            print(self.main_wDir)
            print(self.setup_wDir)

        self.rules1 = open(f'{self.setup_wDir}/config.json', 'r') # self.rules > self.rules1

        # will contain everything from config.json, including environment information
        self.rules = json.load(self.rules1)

        self.rules1.close() # self.rules > self.rules1, didn't close before

        # always runs, mode is not used
        if mode == 0: 

            # assigning vars (local)
            rules_list = [] # checking for whats true in config.json (44-66)

            # iterate through rules dictionary and check for True
            for key in self.rules:
                if self.rules[key] == False:
                    rules_list.append(False)

                else:
                    rules_list.append(True)

                if rules_list.count(True) > 0:
                    pass

                # exit if no True in config.json
                else:
                    print('---------------')
                    print('Running no files; cancelling in 5s')
                    print('---------------')
                    time.sleep(5)
                    exit()
            
            # printing start statement, format, prompting

            # check the rule for shortcut, ignore everything below if so
            f = open(f'{self.setup_wDir}/data.json', 'r')
            data_dict = json.load(f)
            f.close()
            if data_dict['shortcut']:

                if data_dict['update']:
                    print('---------------')
                    print('Installer is in update mode.')

                    if data_dict['bounds'] == 'full':
                        '''
                        flow for full re-install
                        
                            - deletes previous tmp folder in setup
                            - creates new tmp folder
                            - alerts that this installation requires user interaction
                            - download .zip
                            - extract .zip
                            - copy "full-redo" into the directory ABOVE of main
                            - get rid of tmp
                            - reset data.json
                            - provide further instructions on what to do
                            done!
                        '''

                        # FOR PYTHON
                        ut2_wDir = os.path.dirname(os.path.dirname(os.path.dirname(self.setup_wDir)))
                        print(ut2_wDir)

                        # FOR COMPILE
                        #os.path.dirname(ut2_wDir)

                        print('Update: installing full')
                        print('- This is a update that requires a re-installation of all game files.')
                        print('  Nothing will be saved.')
                        print('If you want to backup your files, copy the ENTIRE directory now.')
                        print(f'The directory is: {ut2_wDir}/everything')
                        if input('Continue? (y/n) ').lower() != 'y':
                            print('---------------')
                            print('Cancelling...')
                            print('Update: Resetting data.json...')
                            f = open(f'{self.setup_wDir}/data.json', 'r')
                            td = json.load(f)
                            f.close()
                            td['bounds'] = 'x'
                            td['update'] = False
                            td['shortcut'] = True
                            f = open(f'{self.setup_wDir}/data.json', 'w')
                            json.dump(td, f)
                            f.close()
                            input('Enter anything to exit: ')
                            exit()

                        print('---------------')
                        print('Update: Cleaning tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No prior tmp')
                        print('Update: Making tmp...')
                        os.mkdir(f'{self.setup_wDir}/tmp')


                        print('Update: Cleaning full-redo...')
                        try:
                            shutil.rmtree(f'{ut2_wDir}/full-redo')
                        except:
                            print('Update: No prior full-redo')

                        print('Update: Downloading .zip...')
                        import update.download as update_agent
                        repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
                        zip_download_path = f"{self.setup_wDir}/tmp/latest_release.zip"  # Change the path if needed
                        update_agent.download_latest_release(repo_url, zip_download_path)
                        ext_download_path = f"{self.setup_wDir}/tmp"
                        print('Update: Extracting files...')
                        time.sleep(1)

                        # https://www.geeksforgeeks.org/unzipping-files-in-python/
                        import update.extract as extract_agent
                        extract_agent.extract(zip_download_path, ext_download_path)
                        
                        print('Update: Getting commit label...')
                        release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
                        release_version = release_version.json()
                        release_version = str(release_version['body'])
                        release_version = release_version.split()
                        release_version = release_version[0]

                        # copy full-redo folder ABOVE current installation main, so it is:
                        # root: main, full-redo (in same dir)
                        print('Update: Copying control folder...')
                        copy_source = f"{ext_download_path}/SketchedDoughnut-development-{release_version}/everything/full-redo"
                        dump_location = f'{ut2_wDir}/full-redo'
                        print(f'Update: Copying files to {dump_location}')

                        # https://pynative.com/python-copy-files-and-directories/
                        import update.copy as copy_agent
                        copy_agent.copy(copy_source, dump_location)

                        # clean up tmp
                        print('Update: Cleaning up tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No tmp')

                        # check install path
                        print('Update: Checking install path...')
                        if os.path.exists(f'{ut2_wDir}/full-redo'):
                            pass
                        else:
                            print('!!! UPDATE ERROR: The installed directory does not exist. Cancelling.')
                            input('Enter anything to exit: ')
                            exit()

                        print('---------------')
                        print(f"""Update: Part 1/2 of update is done.
This installer is incapable of finishing this update, as it will require deleting itself. 
In order to finish this install, please go to --
> {ut2_wDir}/full-redo/
-- and run the file named "full-redo.exe". It will run you through the process to finish this update.""")
                        print('---------------')
                        input('Enter anything to exit: ')
                        exit()
                        

                        













                    if data_dict['bounds'] == 'game_data':

                        '''
                        flow for game data re-install

                            - deletes previous "tmp" folder in setup
                            - creates new "tmp folder"
                            - deletes previous "game_data"
                            - downloads .zip
                            - extracts all of .zip
                            - copies "game_data" from the extracted version into proper directory
                            - gets rid of "tmp"
                            - resets "data.json"
                            - done!
                        '''
                        
                        print('Update: installing game_data')
                        print('If you want to backup your game_data, copy the directory now.')
                        print(f'The directory is: {self.main_wDir}/top/container/game_data')
                        if input('Continue? (y/n) ').lower() != 'y':
                            print('---------------')
                            print('Cancelling...')
                            print('Update: Resetting data.json...')
                            f = open(f'{self.setup_wDir}/data.json', 'r')
                            td = json.load(f)
                            f.close()
                            td['bounds'] = 'x'
                            td['update'] = False
                            td['shortcut'] = True
                            f = open(f'{self.setup_wDir}/data.json', 'w')
                            json.dump(td, f)
                            f.close()
                            input('Enter anything to exit: ')
                            exit()

                        print('---------------')
                        print('Update: Cleaning tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No prior tmp')
                        print('Update: Making tmp...')
                        os.mkdir(f'{self.setup_wDir}/tmp')
                        print('Update: deleting previous game_data...')
                        try:
                            shutil.rmtree(f"{self.main_wDir}/top/container/game_data")
                        except:
                            print('Update: No prior game_data')
                        print('Update: Downloading .zip...')
                        import update.download as update_agent
                        repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
                        zip_download_path = f"{self.setup_wDir}/tmp/latest_release.zip"  # Change the path if needed
                        update_agent.download_latest_release(repo_url, zip_download_path)
                        ext_download_path = f"{self.setup_wDir}/tmp"
                        print('Update: Extracting files...')

                        # https://www.geeksforgeeks.org/unzipping-files-in-python/
                        import update.extract as extract_agent
                        extract_agent.extract(zip_download_path, ext_download_path)

                        print('Update: Getting commit label...')
                        #release_version = ((requests.get(("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")).json()['body']))
                        release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
                        release_version = release_version.json()
                        release_version = str(release_version['body'])
                        release_version = release_version.split()
                        release_version = release_version[0]
                        copy_source = f"{ext_download_path}/SketchedDoughnut-development-{release_version}/everything/main/top/container/game_data"
                        copy_location = f'{(self.main_wDir)}/top/container/game_data'
                        print(f'Update: Copying files to {copy_location}')

                        # https://pynative.com/python-copy-files-and-directories/
                        import update.copy as copy_agent
                        copy_agent.copy(copy_source, copy_location)

                        print('Update: Cleaning up tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No tmp')
                        
                        print('Update: Checking install path...')
                        if os.path.exists(f'{self.main_wDir}/top/container/game_data'):
                            pass
                        else:
                            print('!!! UPDATE ERROR: The installed directory does not exist. Cancelling.')
                            input('Enter anything to exit: ')
                            exit()
                        
                        print('Update: Resetting data.json...')
                        f = open(f'{self.setup_wDir}/data.json', 'r')
                        td = json.load(f)
                        f.close()
                        td['bounds'] = 'x'
                        td['update'] = False
                        td['shortcut'] = True
                        f = open(f'{self.setup_wDir}/data.json', 'w')
                        json.dump(td, f)
                        f.close()

                        print('Update: Reaching to version.json...')
                        print(f'Update: Path: {self.main_wDir}/top/container/version.json')
                        #print(release_version)
                        print('Update: Dumping version...')
                        f = open(f'{self.main_wDir}/top/container/version.json', 'w')
                        #print(release_version)
                        json.dump(release_version, f)
                        f.close()

                        print('Update: Reaching to state.json...')
                        print(f'Update: Path: {self.main_wDir}/top/container/state.json')
                        f = open(f'{self.main_wDir}/top/container/state.json', 'r')
                        tmp = json.load(f)
                        f.close()
                        f = open(f'{self.main_wDir}/top/container/state.json', 'w')
                        tmp = False
                        json.dump(tmp, f)
                        f.close()
                        
                        print('Update: Game data update complete!')
                        print('---------------')
                        input('Enter anything to exit: ')
                        exit()









                    if data_dict['bounds'] == 'top':
                        print('---------------')
                        print('Installer is in top mode.')

                        '''
                        flow for game data re-install

                            - deletes previous "tmp" folder in setup
                            - creates new "tmp folder"
                            - deletes previous "top"
                            - downloads .zip
                            - extracts all of .zip
                            - copies "top" from the extracted version into proper directory
                            - gets rid of "tmp"
                            - resets "data.json"
                            - done!
                        '''
                        
                        print('Update: installing top')
                        print('If you want to backup the top directory,, copy the directory now.')
                        print(f'The directory is: {self.main_wDir}/top')
                        if input('Continue? (y/n) ').lower() != 'y':
                            print('---------------')
                            print('Cancelling...')
                            print('Update: Resetting data.json...')
                            f = open(f'{self.setup_wDir}/data.json', 'r')
                            td = json.load(f)
                            f.close()
                            td['bounds'] = 'x'
                            td['update'] = False
                            td['shortcut'] = True
                            f = open(f'{self.setup_wDir}/data.json', 'w')
                            json.dump(td, f)
                            f.close()
                            input('Enter anything to exit: ')
                            exit()

                        print('---------------')
                        print('Update: Cleaning tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No prior tmp')
                        print('Update: Making tmp...')
                        os.mkdir(f'{self.setup_wDir}/tmp')
                        print('Update: deleting previous top...')
                        try:
                            shutil.rmtree(f"{self.main_wDir}/top")
                        except:
                            print('Update: No prior top')
                        print('Update: Downloading .zip...')
                        import update.download as update_agent
                        repo_url = "https://api.github.com/repos/SketchedDoughnut/development/releases/latest"
                        zip_download_path = f"{self.setup_wDir}/tmp/latest_release.zip"  # Change the path if needed
                        update_agent.download_latest_release(repo_url, zip_download_path)
                        ext_download_path = f"{self.setup_wDir}/tmp"
                        print('Update: Extracting files...')

                        # https://www.geeksforgeeks.org/unzipping-files-in-python/
                        import update.extract as extract_agent
                        extract_agent.extract(zip_download_path, ext_download_path)

                        print('Update: Getting commit label...')
                        #release_version = ((requests.get(("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")).json()['body']))
                        release_version = requests.get("https://api.github.com/repos/SketchedDoughnut/development/releases/latest")
                        release_version = release_version.json()
                        release_version = str(release_version['body'])
                        release_version = release_version.split()
                        release_version = release_version[0]
                        copy_source = f"{ext_download_path}/SketchedDoughnut-development-{release_version}/everything/main/top"
                        copy_location = f'{(self.main_wDir)}/top'
                        print(f'Update: Copying files to {copy_location}')

                        # https://pynative.com/python-copy-files-and-directories/
                        import update.copy as copy_agent
                        copy_agent.copy(copy_source, copy_location)

                        print('Update: Cleaning up tmp...')
                        try:
                            shutil.rmtree(f'{self.setup_wDir}/tmp')
                        except:
                            print('Update: No tmp')
                        
                        print('Update: Checking install path...')
                        if os.path.exists(f'{self.main_wDir}/top'):
                            pass
                        else:
                            print('!!! UPDATE ERROR: The installed directory does not exist. Cancelling.')
                            input('Enter anything to exit: ')
                            exit()
                        
                        print('Update: Resetting data.json...')
                        f = open(f'{self.setup_wDir}/data.json', 'r')
                        td = json.load(f)
                        f.close()
                        td['bounds'] = 'x'
                        td['update'] = False
                        td['shortcut'] = True
                        f = open(f'{self.setup_wDir}/data.json', 'w')
                        json.dump(td, f)
                        f.close()

                        print('Update: Reaching to version.json...')
                        print(f'Update: Path: {self.main_wDir}/top/container/version.json')
                        #print(release_version)
                        print('Update: Dumping version...')
                        f = open(f'{self.main_wDir}/top/container/version.json', 'w')
                        #print(release_version)
                        json.dump(release_version, f)
                        f.close()

                        print('Update: Reaching to state.json...')
                        print(f'Update: Path: {self.main_wDir}/top/container/state.json')
                        f = open(f'{self.main_wDir}/top/container/state.json', 'r')
                        tmp = json.load(f)
                        f.close()
                        f = open(f'{self.main_wDir}/top/container/state.json', 'w')
                        tmp = False
                        json.dump(tmp, f)
                        f.close()
                        
                        print('Update: top update complete!')
                        print('---------------')
                        input('Enter anything to exit: ')
                        exit()




















                else:
                    print('---------------')
                    print('Installer redirecting to starter file...')

                    # FOR PYTHON
                    self.top_wDir = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                    # FOR COMPILE
                    self.top_wDir = os.path.dirname(self.top_wDir)

                    self.top_wDir = os.path.join(self.top_wDir, 'top')
                    os.system(f'python {self.top_wDir}/starter.py')
                    exit() 












            print('---------------')
            print("""
            Welcome to the open-source installer created by Sketched Doughnut! 
                Code is written by Sketched Doughnut with snippets from others.
                   Sources are in: (install location)/gitignore/sources.txt.   
            """)
            path_loop = True
            while path_loop:
                print('---------------')
                print(f"""Input file directory for install below (or type "delete" to delete).'
Note: Must be absolute path. Ex: C:\\folder\\install_location.""") # Enter nothing for default installation path (in Program Files).
                self.install_path = input('--> ')

                # checking for uninstall, doing uninstall if so
                if self.install_path == "delete":
                    print('---------------')
                    if input('Are you sure you want to delete?  \nType: "confirm-delete", anything else to cancel \n--> ') == 'confirm-delete':

                        # for run
                        if self.rules['env'] == 'run':
                            os.system(f'python {self.main_wDir}/delete.py')

                        # - for codespace
                        else:
                            os.system(f'python main/setup/delete.py')

                        # final, then finishes
                        print('---------------')
                        # print('Delete done. This installer will exit in 30 seconds; afterwards, delete the folder it is in. Thank you for using this installer! :3')
                        # time.sleep(15)
                        # for i in range(15, 0, -1):
                        #     print(i)
                        #     time.sleep(1)
                        print('Delete done. You can now get rid of any installer files. Thank you for using this installer! :3')
                        input('Enter anything to exit: ')
                        exit()
                
                    # cancelling uninstall if wrong input
                    else:
                        print('Cancelling deletion, cancelling file in 5s...')
                        for i in range(5, 0, -1):
                            print(i)
                            time.sleep(1)
                        exit()

                else:

                    # formatting file path
                    try:
                        self.install_path = self.install_path_format(self.install_path)
                        path_loop = self.install_path[1]
                        self.install_path = self.install_path[0]

                    except Exception as e:
                        print('---------------')
                        print(f'Path formatting error: {e}')
                        print('Please restart installer and enter the correct path.')
                        input('Enter anything to exit: ')
                        exit()
                    print('---------------')
                        


    # format install path
    def install_path_format(self, path):
        # try:
        #     programFiles = os.path.abspath("Program Files")
        #     if not path:
        #         print('Path is defaulting to Program Files.')
        #         path = programFiles
        #         path += '\game_name'
        #         return path

        if not path:
            print('Path is defaulting to Program Files.')
            try:
                path = os.path.abspath("Program Files")
                path = os.path.join(os.environ['SystemDrive'], 'Program Files')
                ns = ''
                next = False
                for letter in path:
                    if next == False:
                        ns += letter

                    if next == True:
                        ns += '/'
                        ns += letter
                        next = False

                    if letter == ':':
                        next = True

                    else:
                        next = False
                path = ns
        
            except Exception as e:
                print(f'Default path error: {e}')

        new_string = ''
        list = []

        list = [str(i) for i in path]
        for i in list:
            if i == '\\':
                new_string += '/'
            else:
                new_string += i

        path = new_string
        path = [str(i) for i in path]
        if path[len(path) - 1] == '/':
            path.pop(len(path) - 1)

        else:
            pass

        new_string = ''
        for i in path:
            new_string += i
        path = new_string

        if os.path.exists(path):
            path += '/game_name'
            return [path, False]
    
        else:
            print('---------------')
            print('---------------')
            print('Improper path. Please try again.')
            return [path, True]
        

    # making sure they are sure of their choice
    def safety_check(self):
        print(f"""
              You are running the installer; this will overwrite pre-existing files created by the installer previously
                                        inside of {self.install_path}.
                                To confirm, type "confirm" below. Otherwise, type anything else.
              """)
        
        # checking if input confirms proceeding, cancelling if not
        if input('--> ') == "confirm":
            print('---------------')
            pass

        # cancels program if doesn't confirm clearing
        else:
            print('Cancelling...')
            time.sleep(2)
            exit()


    # cleaning before any running
    def pre_clean(self, run_error=''):
        if run_error == 'error':
        
            # removing install tree
            try:
                shutil.rmtree(self.install_path)
                print(f'Pre: ! install cleaned')
            except:
                print(f'Pre: ! no install')

        else:
            print('Pre: Cleaning up directories before install')

            # removing install tree
            try:
                print(f'Deleting from: {self.install_path}')
                if input('Continue? (y/n) ').lower() == 'n':
                    print('Cancelling...')
                    time.sleep(5)
                    exit()
                    
                shutil.rmtree(self.install_path)
                print(f'! install cleaned')
            except:
                print(f'! no install')

            print('Pre: Done cleaning; continuing...')
            time.sleep(1)
            print('---------------')

    
    # getting info
    def setup(self):
        # getting inputs
        # https://github.com/BirdLogics/sb3topy
        #    self.url = input('Input repository URL: ')
        #    self.branch = input('Input respository branch: ')
        self.desktop_shortcut = (input('Do you want to add a desktop shortcut? (y/n) \n--> ').lower()) == 'y'
        
        # make sure they have python installed
        print('---------------')
        print("""
                     Before we proceed, you need to have an installation of python installed.
              If you already have one, type "y" to proceed. If you don't, do the following instructions:
              - go to Microsoft Store
              - search "Python 3.11"
              - Install
              - You're done!
                        Once done doing these instructions, type 'y' (anything else to cancel).
                       NOTE: FUNCTIONALITY CAN NOT BE GUARANTEED WITH ANY OTHER PYTHON VERSIONS.
              """)
        if input('--> ').lower() != 'y':
            exit()

        else:
            state = ''
            loop1 = True
            loop2 = True

            while loop1:
                print('---------------')
                print(f"""Install info:
                      
        - location: {self.install_path}
        - shortcut: {self.desktop_shortcut}

If these are incorrect, type the name of what you want to re-enter. For example:
"shortcut" or "location"
Otherwise, enter 'y' to continue.""")
                
                loop2 = True
                while loop2:
                    choice = input('--> ').lower()
                    print('---------------')

                    if choice == 'y':
                        state = 'y'
                        loop1 = False
                        loop2 = False

                    elif choice == 'shortcut':
                        state = 'shortcut'
                        loop2 = False
                    
                    elif choice == 'location':
                        state = 'location'
                        loop2 = False

                    else:
                        print('Wrong input. Try again.')
                    
                if state == 'y':
                    loop1 = False

                elif state == 'shortcut':
                    print("input 'y' if you want a shortcut, 'n' if you don't.")
                    self.desktop_shortcut = input('--> ').lower() == 'y'
                    print(f'Shortcut changed to: {self.desktop_shortcut}')
                
                elif state == 'location':
                    print('input the absolute path to the installation location.')
                    self.install_path = self.install_path_format(input('--> '))
                    print(f'path changed to: {self.install_path}')
                

    # create temp dir and establish code file
    def create(self):

        # creating directories
        print(f'Creating directory: {self.install_path}')
        os.mkdir(self.install_path)

        # opening delete file and writing path
        print('Dumping delete path...')
        # for run
        if self.rules['env'] == 'run':
            data = open(f'{self.setup_wDir}/data.json', 'r')
        
        # - for codespace
        else:
            data = open('main/setup/data.json', 'r')

        data_content = json.load(data)
        data.close()
        data_content["remove_path"] = self.install_path

        # for run
        if self.rules['env'] == 'run':
            data = open(f'{self.setup_wDir}/data.json', 'w')

        # - for codespace
        else:
            data = open('main/setup/data.json', 'w')

        json.dump(data_content, data)
        data.close()


    # https://www.blog.pythonlibrary.org/2010/01/23/using-python-to-create-shortcuts/ -> example 3
    def createShortcut(self, path, target='', wDir='', icon=''):  
        from win32com.client import Dispatch
        ext = path[-3:]
        if ext == 'url':
            #shortcut = file(path, 'w')
            shortcut = open(path, 'w')
            shortcut.write('[InternetShortcut]\n')
            shortcut.write('URL=%s' % target)
            shortcut.close()
        else:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            if icon == '':
                pass
            else:
                shortcut.IconLocation = icon
            shortcut.save()


   # function to download incorporating class: https://github.com/fbunaren/GitHubFolderDownloader
    def download(self):

        # initializing the downloader class
        # NOTE: Alternatively, initialize .Downloader empty and instead do load repository with url
        # NOTE: Do this because you can link branch in that url and it will identify it
        # NOTE: .download still runs the same
        try:
            downloader = Downloader("https://github.com/SketchedDoughnut/development")
            #downloader = Downloader("https://github.com/a16z/ai")
            #downloader = Downloader("https://github.com/microsoft/AI")

            # downloading
            try:
                self.start = timeit.default_timer()
                downloader.download(self.install_path)

                # writing run path to text file (not used, not up to date)
                try:
                    print('Assembling text file...')
                    url_path = f'{self.install_path}/everything/main/top/content_url.txt'
                    f = open(url_path, 'w')
                    f.write(f'{self.install_path}/everything/main/top/game_data/main.py')
                    f.close()

                except Exception as e:
                    print(f'Error with text file: {e}')

                # formats info and runs shortcut making function
                try:
                    if self.desktop_shortcut == True:
                        #print('---------------')
                        print('Deleting previous shortcut...')
                        try:
                            os.remove(path)
                        except:
                            print('No prior shortcut.')
                        
                        time.sleep(0.25)
                            
                        import winshell
                        print('Creating shortcut...')
                        desktop = winshell.desktop()
                        
                        path = os.path.join(desktop, "game_name.lnk") # CHANGE game_name TO NAME
                        self.abs_shortcut = path
                        #target = f"{self.install_path}/main/top/starter.exe" # CHANGE TO EXE
                        target = f"{self.install_path}/everything/main/setup/fiesta.exe" # CHANGE TO EXE
                        wDir = f"{self.install_path}/everything/main/setup"
                        #icon = f"{self.install_path}/main/top/starter.exe" # CHANGE TO EXE
                        icon = f"{self.install_path}/everything/main/setup/fiesta.exe" # CHANGE TO EXE

                        # calls on function here with data from above
                        self.createShortcut(target=target, path=path, wDir=wDir, icon=icon)
                        print('Dumping shortcut path...')

                        # run
                        if self.rules['env'] == 'run':
                            f = open(f'{self.setup_wDir}/data.json', 'r')

                        # - for codespace
                        else:
                            f = open('main/setup/data.json', 'r')

                        temp = json.load(f)
                        temp['abs_shortcut'] = self.abs_shortcut
                        f.close()

                        # run
                        if self.rules['env'] == 'run':
                            f = open(f'{self.setup_wDir}/data.json', 'w')

                        # - for codespace
                        else:
                            f = open('main/setup/data.json', 'w')
                            
                        json.dump(temp, f)
                        f.close()
                            
                    else:
                        pass

                except Exception as e:
                    print(f'Error creating shortcut: {e}')

            except Exception as e:
                print(f'!!! Error while downloading: {e}')
                #print('Cleaning up then exiting...')
                #self.pre_clean('error')
                #exit()

        except Exception as e:
            print(f'!!! Error while creating object: {e}')
            #print('Consider re-entering branch name / github url')
            #print('Cleaning up then exiting...')
            #self.pre_clean('error')
            #exit()    
        self.end = timeit.default_timer()     


    # doing file cleanup
    def post_clean(self):
        print('---------------')
        print('Post: Cleaning up')
        print('Post: Deleting extra files...')

        # remove setup folder
        if self.rules['env'] == 'run':
            shutil.rtmree(f'{self.install_path}/setup')
            os.remove(f'{self.install_path}/top/content_url.txt')

        else:
            print('Individual cleanup is not offered for this mode. Use mode run instead')

        print('Post: Extra files deleted.')

        ## to delete setup folder if needed (not used)
        #shutil.rmtree(f'{self.install_path}/main/setup')

        #shutil.rmtree('./temp/')
        print('Post: Note: If directory is not present, or is empty, check your inputs and run again.')
        print('Post: Done cleaning; continuing...')


    # quits install file (to make sure it goes right)
    def quit_install(self):
        print('---------------')
        input(f'Install complete! Time: {round(self.end - self.start, 2)}s \nEnter anything to exit: ')
        #print('Install complete. Exit in:')
        #for i in range(3, 0, -1):
        #    print(f'{i}')
        #    time.sleep(1)

        # ensure an exit happens
        exit()

    # more of an assurance honestly, but eh
    def edit_data(self):
        print('---------------')
        print('Updating installed data.json...')
        f = open(f'{self.install_path}/everything/main/setup/data.json', 'r')
        content = json.load(f)
        f.close()
        content['shortcut'] = True
        content['update'] =  False
        content['bounds'] = 'x'
        f = open(f'{self.install_path}/everything/main/setup/data.json', 'w')
        json.dump(content, f)
        f.close()
        print('Installed data.json updated.')


    # runs all the functions in order, by config rules (can be changed in config.json)
    def run(self):

        if self.rules['safety_check']: self.safety_check()
        if self.rules['pre_clean']: self.pre_clean()
        if self.rules['setup']: self.setup()
        if self.rules['create']: self.create()
        if self.rules['download']: self.download()
        if self.rules['post_clean']: self.post_clean()
        if self.rules['edit_data']: self.edit_data()
        if self.rules['quit_install']: self.quit_install()


########################################################################

########################################################################
########################################################################
########################################################################
    
#!/usr/bin/python
# -*- coding: utf-8 -*-

'''

GitHub Folder Downloader
Created by Fransiscus Emmanuel Bunaren
https://bunaren.com
'''

class Downloader:

    def __init__(self, repository_url='', branch=''):
        if not repository_url:
            self.repo_url = ''
            self.files = []
            self.location = dict()
        else:
            self.load_repository(repository_url, branch)

    @classmethod
    def __get_branch_from_url(self, url, branch=''):
        if '/tree/' in url and not branch:
            branch = url.split('/tree/')[1]
            branch = branch.split('/')[0]
        else:
            branch = 'master'
        return branch

    @classmethod
    def __get_raw_url(self, file_path, url, branch=''):
        tmp_url = url.replace(
            'https://api.github.com/repos/',
            'https://raw.githubusercontent.com/')
        tmp_url = tmp_url.split('/git/blobs/')[0]
        tmp_url = tmp_url + '/' + branch + '/' + file_path
        return tmp_url

    def load_repository(self, url, branch=''):

        # Check if URL contains branch name

        branch = self.__get_branch_from_url(url, branch)

        # Convert URL to match GitHub API URI

        tmp_url = url.replace('https://github.com/',
                            'https://api.github.com/repos/')
        tmp_url += '/git/trees/{}?recursive=1'.format(branch)

        # Make GET Request

        api = requests.get(tmp_url).text
        files = json.loads(api)

        # Turn the API Data into List

        output = []
        location = dict()
        for (k, i) in enumerate(files['tree']):
            if i['type'] == 'blob':
                tmp = [i['path']]

                # Get RAW URL

                tmp += [self.__get_raw_url(tmp[0], i['url'], branch)]
                output.append(tmp)
            else:
                location[i['path']] = k
        self.files = output
        self.location = location

        # Set Repo URL for memoization

        self.repo_url = url

    def __mkdirs(self, path):

        # Make directory if not exist

        if not os.path.isdir(path):
            os.makedirs(path)

    def download(
        self,
        destination,
        target_folder='*',
        recursive=True,
    ):

        # Make directory if not exist

        self.__mkdirs(destination)

        # Find Folder Position

        if target_folder == '*':
            start = 0
        else:

            # Remove Relative Path Symbol from string

            tmp_target = target_folder.replace('./', '')
            tmp_target = tmp_target.replace('../', '')

            # Remove "/"

            tmp_target = (tmp_target if tmp_target[-1] != '/'
                        else tmp_target[:-1])
            start = self.location[target_folder]

        # Start Downloading

        for i in self.files[start:]:
            try:
                if recursive or i[0].split(target_folder)[1].count('/') \
                        <= 1:
                    self.__mkdirs(destination + '/' + os.path.dirname(i[0]))
                    urllib.request.urlretrieve(i[1], destination + '/' + i[0])

                    # modified segment by me
                    print(f'- Installing file: /{i[0]}')
            except Exception as e:
                print(f'File download error: {e}')


########################################################################
########################################################################
########################################################################


## ONLY TWO ACTING LINES OF CODE
# initializes Install class
install = Install()

# calls on run function
install.run()