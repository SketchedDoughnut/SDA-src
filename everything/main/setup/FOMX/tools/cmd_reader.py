#imports
import os
import shutil

def read_commands(above_everything_dir, cmd_dir) -> None:
    f = open(cmd_dir, 'r')
    cmds = f.readlines()
    f.close()

    for cmdd in cmds:
        line = cmdd.split()
        cmd = line[0]
        dir = line[1]
        if cmd == 'mkdir':
            os.mkdir(os.path.join(above_everything_dir, dir))
        elif cmd == 'rmdir':
            shutil.rmtree(os.path.join(above_everything_dir, dir))
        elif cmd == 'mkfile':
            f = open(os.path.join(above_everything_dir, dir), 'w')
            f.close()
        elif cmd == 'rmfile':
            os.remove(os.path.join(above_everything_dir, dir))