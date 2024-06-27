import threading
import os
import time
import sys
import random

def run_file(path):
    os.system(f'python {path}')

def thread_test(sample):
    for i in range(10):
        print(sample, random.randint(0,100))

# file tests
threading.Thread(target=lambda: run_file('gitignore/render/3d_terrain.py')).start()
#print('------------------')
threading.Thread(target=lambda: run_file('main/setup/fiesta.exe')).start()
    
# normal function threads
num = 1
threading.Thread(target=lambda: thread_test(num)).start()
num = 2
threading.Thread(target=lambda: thread_test(num)).start()

# print(threading.active_count())
# methods to exit a thread: 
    # https://superfastpython.com/thread-close/#:~:text=python%20concurrency%20APIs%3F-,Close%20Thread%20By%20Raising%20an%20Exception,then%20terminate%20the%20new%20thread.
    #sys.exit()
    #raise Exception('close')
    #return 