# a copy of the propagator for FOMX, which is ran last
# this file is only imported right after use, so that it can be updated by FOMX

# this file propagates the one template copy of the crash handler to every other crash handler
# it is built for use with VSCode because paths are wonky
########################################################################
def propagate_crash_handler(wDir):
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

    f = open(wDir +  crash_source, 'r')
    crash_source_content = f.read()
    f.close()
    print('-> FOMX: Getting contents of source...')

    for file in raw_crash_file_list:
        f = open(wDir + file, 'w')
        f.write(crash_source_content)
        f.close()
        print('-> FOMX: Propogating to raw file:', file)

    for file in compiled_crash_file_list:
        f = open(wDir + file, 'w')
        f.write(crash_source_content)
        f.close()
        print('-> FOMX: Propogating to compiled file:', file)


def propagate_elevator(wDir):
    raw_elevator_file_list = [
        r'everything\main\top\container\index_elevator.py'
    ]

    elevator_source = r'everything\gitignore\dev\elevator.py'

    f = open(wDir + elevator_source, 'r')
    elevator_source_content = f.read()
    f.close()
    print('-> FOMX: Getting contents of source...')

    for file in raw_elevator_file_list:
        f = open(wDir + file, 'w')
        f.write(elevator_source_content)
        f.close()
        print('-> FOMX: Propogating to raw file:', file)


def propagate_master(wDir, elevator: bool = False, crash: bool = False):
    wDir += '\\'
    if elevator:
        propagate_elevator(wDir)
    if crash:
        propagate_crash_handler(wDir)