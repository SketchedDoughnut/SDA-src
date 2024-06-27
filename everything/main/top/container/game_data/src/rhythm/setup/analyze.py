file1 = input('Input file 1: ')
file2 = input('Input file 2: ')

# get files length
f = open(file1, 'r')
file1_length = len(f.read())
file1_list = list(f.read())
f.close()
f = open(file2, 'r')
file2_length = len(f.read())
file2_list = list(f.read())
f.close()

# print
print(f'Length of file 1: {file1_length}')
print(f'Length of file 2: {file2_length}')

f1_l_f2 = file1_length < file2_length
f1_g_f2 = file1_length > file2_length

print('\nStatus:')
print('File 1 is greater then file 2:', f1_g_f2)
print('File 1 is less then file 2:', f1_l_f2)

if f1_g_f2:
    print('\nIt appears file 1 has more content then file 2. File 2 will be boosted to match file 1.')
    input('Enter anything to continue: ')
    while file2_length < file1_length:
        file2_list.append([0.001, False])
        file2_length = len(file2_list)

    print(f'\nLength of file 1: {file1_length}')
    print(f'Length of file 2: {file2_length}')

if f1_l_f2:
    print('\nIt appears file 1 has less content then file 2. File 1 will be boosted to file 2.')
    input('Enter anything to continue: ')
    while file1_length < file2_length:
        file1_list.append([0.001, False])
        file1_length = len(file1_list)

    print(f'\nLength of file 1: {file1_length}')
    print(f'Length of file 2: {file2_length}')

print('\nRewriting both files.')
input('Enter anything to continue: ')

import json
f = open(file1, 'w')
json.dump(file1_list, f)
f.close()
print('\nFile one dumped. Moving to two')
input('Enter anything to continue: ')

f = open(file2, 'w')
json.dump(file2_list, f)
f.close()
print('\nDone. Re-evaluating files.')

f = open(file1, 'r')
file1_length = len(f.read())
f.close()
f = open(file2, 'r')
file2_length = len(f.read())
f.close()

print(f'\nLength of file 1: {file1_length}')
print(f'Length of file 2: {file2_length}')