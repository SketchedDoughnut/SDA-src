### imports
import winshell
import os
import shutil
import time
import timeit

# downloader imports
import json
import requests
import urllib


##########################################################################################
##########################################################################################


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
                    print(f'- Installing file: /{i}')

            except Exception as e:
                print(f'File download error: {e}')


#########################################################################################################
## create directory on desktop
desktop = winshell.desktop()

## install location
path = f'{desktop}/flash-inst'

## prints
print('-----------------------------------')
print(f'Creating directory on desktop: {desktop}')
print(f'Full install path: {path}')
print('Downloading...')
print('-----------------------------------')
time.sleep(3)

## ask to delete any previous installations
if os.path.exists(path):
    if input('Previous installation found. Delete? (y/n) ').lower() == 'y':
        shutil.rmtree(path)
        print('-----------------------------------')
        if input('Enter y to continue, or n to quit: ').lower() == 'n':
            exit()
        else:
            print('-----------------------------------')
            time.sleep(1)
        
    else:
        print('-----------------------------------')
        input('Cancelled. Enter anything to exit: ')

## make downloader obj with github url
downloader = Downloader("https://github.com/SketchedDoughnut/development")

## make install dir
os.mkdir(path)

## download in location
# start time elapsing
# https://www.programiz.com/python-programming/examples/elapsed-time
start = timeit.default_timer()

try:
    downloader.download(f'{desktop}/flash-inst')

except Exception as e:
    print(f'Download error: {e}')

# end time elapsing
end = timeit.default_timer()

# calc
elapsed = round(end - start, 2)

# print elapsed
print('-----------------------------------')
print(f'Total time taken: {elapsed}s')
input('Enter anything to exit: ')