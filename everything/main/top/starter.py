# the code god has spited me :c

import os

#wDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#path = os.path.join(wDir, 'top/container/index.py')
wDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(wDir, 'container/index.py')
print('----------------------------')
print(path)

print('Starter redirecting to index file...')
print('----------------------------')
c1 = r'python {patth}'.format(patth=path) # calling string
# os.system(f'python {path}')
os.system(c1)