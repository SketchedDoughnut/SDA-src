

def try_pretty_print():
    '''
    NOTES
    - https://stackoverflow.com/questions/35850362/importerror-no-module-named-curses-when-trying-to-import-blessings
    - https://stackoverflow.com/questions/64289140/print-updated-string-without-showing-previous-one
    '''
    import time
    import curses
    screen = curses.initscr()
    now = time.time()
    future = now + 10
    while time.time() < future:
        screen.erase()
        screen.addstr(str(time.time()))
        screen.refresh()
        pass
    curses.endwin()

def test_clear_print():
    import sys
    # https://stackoverflow.com/questions/5426546/in-python-how-to-change-text-after-its-printed    
    '''
        print 'hello',
        sys.stdout.flush()
        ...
        print '\rhell ',
        sys.stdout.flush()
    '''
    print('hello')
    sys.stdout.flush()
    print ('\rhell')
    sys.stdout.flush()