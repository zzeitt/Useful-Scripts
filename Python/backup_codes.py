import os
import shutil
import glob


def backUpCodes(dir_bak):
    dir_cur = os.path.dirname(os.path.abspath(__file__))
    li_pys = [f for f in glob.glob(f'{dir_cur}/*.py', recursive=False)]
    for i in li_pys:
        shutil.copyfile(i, os.path.join(dir_bak, os.path.basename(i)))
