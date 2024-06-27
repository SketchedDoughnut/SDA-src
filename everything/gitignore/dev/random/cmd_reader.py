# to read commands
f = open(input('abs path: '), 'r')
cmds = f.readlines()
f.close()

for line in cmds:
    line = line.split()
    cmd = line[0]
    dir = line[1]
    print('cmd:', cmd)
    print('dir:', dir)
    print('! ---------- end of line ---------- !')