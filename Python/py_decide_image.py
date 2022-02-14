import os
import cv2
from tqdm import tqdm
import numpy as np
import fire
from get_file_paths import getFilePaths


def main(dir_src, dir_dst):
    li_srcs = getFilePaths(dir_src)
    li_dsts = getFilePaths(dir_dst)

    for idx, s_src in enumerate(tqdm(li_srcs)):
        # if idx >= 5000:
        #     break
        
        s_dst = li_dsts[idx]
        cv_src = cv2.imread(s_src)
        cv_dst = cv2.imread(s_dst)
        cv_show = np.concatenate((cv_src, cv_dst), axis=1)
        name = os.path.basename(s_src)
        cv2.namedWindow(name, cv2.WINDOW_KEEPRATIO)
        cv2.resizeWindow(name, 2048, 600)
        cv2.imshow(name, cv_show)
        k = cv2.waitKey(0)
        if k == ord('d'):
            print('====> Image passed...')
            cv2.destroyWindow(name)
        elif k == ord('s'):
            print(f'====> Key `s` pressed.')
            cv2.destroyWindow(name)
        elif k == ord('q'):
            break
        
if __name__ == '__main__':
    fire.Fire(main)
