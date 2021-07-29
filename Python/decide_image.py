import os
import cv2
from tqdm import tqdm
import numpy as np


def getFilePaths(path):
    # read a folder, return the complete path
    ret = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            ret.append(os.path.join(root, filespath))
    ret.sort()
    return ret

pth_src = './src'
pth_dst = './dst'
li_srcs = getFilePaths(pth_src)
li_dsts = getFilePaths(pth_dst)
li_srcs.sort(key=lambda x: int(os.path.basename(x)[:-4]))
li_dsts.sort(key=lambda x: int(os.path.basename(x)[:-4]))

for idx, s_src in enumerate(tqdm(li_srcs)):
    if idx >= 5000:
        break
    
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
        s_src_arch = s_src.replace('src', 'shape_before')
        s_dst_arch = s_dst.replace('dst', 'shape_after')
        cv2.imwrite(s_src_arch, cv_src)
        cv2.imwrite(s_dst_arch, cv_dst)
        print(f'====> Image archived at: <{s_src_arch}> <{s_dst_arch}>')
        cv2.destroyWindow(name)
    elif k == ord('q'):
        break
    
