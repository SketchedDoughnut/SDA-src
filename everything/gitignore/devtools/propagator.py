# this file propagates the one template copy of the crash handler to every other crash handler
# it is built for use with VSCode because paths are wonky
########################################################################
def propagate_crash_handler():
    raw_crash_file_list = [
        r'everything\main\top\container\index_crash_handler.py',
        r'everything\main\top\container\game_data\src\conways-game\conway_crash_handler.py',
        r'everything\main\top\container\game_data\src\flappy\flappy_crash_handler.py',
        r'everything\main\top\container\game_data\src\rhythm\rhythm_crash_handler.py'
    ]

    compiled_crash_file_list = [
        r'everything\main\setup\setup_crash_handler.py'
    ]

    crash_source = r'everything\gitignore\dev\crash_handler.py'

    f = open(crash_source, 'r')
    crash_source_content = f.read()
    f.close()
    print('Getting contents of source...')

    for file in raw_crash_file_list:
        f = open(file, 'w')
        f.write(crash_source_content)
        f.close()
        print('Propogating to raw file:', file)

    for file in compiled_crash_file_list:
        f = open(file, 'w')
        f.write(crash_source_content)
        f.close()
        print('Propogating to compiled file:', file)


def propagate_elevator():
    raw_elevator_file_list = [
        r'everything\main\top\container\index_elevator.py'
    ]

    elevator_source = r'everything\gitignore\dev\elevator.py'

    f = open(elevator_source, 'r')
    elevator_source_content = f.read()
    f.close()
    print('Getting contents of source...')

    for file in raw_elevator_file_list:
        f = open(file, 'w')
        f.write(elevator_source_content)
        f.close()
        print('Propogating to raw file:', file)



running = input('-> ')
if running == '1':
    propagate_crash_handler()
elif running == '2':
    propagate_elevator()