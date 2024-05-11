import os
import json
# import shutil
# import time
# import py_compile # interesting thing

def verify_files(json_path, everything_path):
    # vars
    failed = False
    failed_count = 0

    # load files
    f = open( json_path, 'r')
    files = json.load(f)
    f.close()

    for file in files:
        assemble = os.path.join(os.path.dirname(everything_path), file)
        #assemble = os.path.join(everything_path, file)
        if os.path.exists(assemble):
            #print(f'- verified {files.index(file) + 1}/{len(files)} - {assemble}')
            pass
        else:
            print(f'- FILE DOES NOT EXIST: {assemble}')
            failed_count += 1
    if failed_count > 0:
        failed = True
        print('------------------------------------')
        print('- It appears that 1 or more files are missing. This update will cancel, and instead reload your backup.')
        print('------------------------------------')
        # break
    return failed