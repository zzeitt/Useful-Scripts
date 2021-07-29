import cv2
import numpy as np
import os


def doColorMask(base, bmask, opacity=0.65, bgr=(0, 0, 255)):
    cmask = base.copy()
    bgr = np.asarray(bgr)
    cmask[bmask] = cmask[bmask]*opacity + bgr*(1-opacity)
    return cmask

if __name__ == "__main__":
    for i in range(0, 50):
        num = i
        
        s_mask = ('/home/zeit/SDC/NiseProgPool/forGit/forFakeDetection/2019-CVPR-ManTraNet/results')
        s_cont = ('/home/zeit/SDC/NiseProgPool/forGit/forSteganalysis/images/Paris_unshuffle/')
        s_secr = ('/home/zeit/SDC/NiseProgPool/forGit/forSteganalysis/images/Paris_unshuffle/Paris_secrs')
        
        # s_mask_hips = os.path.join(s_mask, 'Paris_HIPS_epoch-800000_sz-227')
        # s_cont_hips = os.path.join(s_cont, 'Paris_HIPS_epoch-800000_sz-227')
        # s_mask_inn = os.path.join(s_mask, 'Paris_INN_epoch-300000_sz-227')
        # s_cont_inn = os.path.join(s_cont, 'Paris_INN_epoch-300000_sz-227')
        
        # name_cont_mask = f'{num:03}_cont_mask.png'
        # name_secr = f'{num:03}_secr_{(num+51):03}_im.png'
        # name_cont = f'{num:03}_cont.png'
        
        s_mask_inn = os.path.join(s_mask, 'Paris_inn_new')
        s_cont_inn = os.path.join(s_cont, 'Paris_inn_new')

        name_cont_mask = f'{(num+1):03}_im_forw_H_mask.png'
        name_secr = f'{num:03}_secr_{(num+51):03}_im.png'
        name_cont = f'{(num+1):03}_im_forw_H.png'
        
        # cv_mask_hips = cv2.imread(os.path.join(s_mask_hips, name_cont_mask), cv2.IMREAD_GRAYSCALE)
        # cv_cont_hips = cv2.imread(os.path.join(s_cont_hips, name_cont))
        # b_mask_hips = (cv_mask_hips > 128)
        
        cv_mask_inn = cv2.imread(os.path.join(s_mask_inn, name_cont_mask), cv2.IMREAD_GRAYSCALE)
        cv_cont_inn = cv2.imread(os.path.join(s_cont_inn, name_cont))
        b_mask_inn = (cv_mask_inn > 128)
            
        cv_secr = cv2.imread(os.path.join(s_secr, name_secr))
        cv_secr = cv2.resize(cv_secr, (cv_cont_inn.shape[0], cv_cont_inn.shape[1]))

        # cmask_secr_hips = doColorMask(cv_secr, b_mask_hips)
        # cmask_cont_hips = doColorMask(cv_cont_hips, b_mask_hips)
        
        cmask_secr_inn = doColorMask(cv_secr, b_mask_inn)
        cmask_cont_inn = doColorMask(cv_cont_inn, b_mask_inn)
        
        # cv2.imshow('cmask_secr_hips', cmask_secr_hips)
        # cv2.imshow('cmask_cont_hips', cmask_cont_hips)
        # cv2.imshow('cmask_secr_inn', cmask_secr_inn)
        # cv2.imshow('cmask_cont_inn', cmask_cont_inn)
        
        s_save = (
            '/home/zeit/SDB/NiseEngFolder/forLaTeX/20201019_INV_STEG_fig/images_mantranet')
        # cv2.imwrite(os.path.join(
        #     s_save, f'{num}_cmask_secr_hips.png'), cmask_secr_hips)
        # cv2.imwrite(os.path.join(
        #     s_save, f'{num}_cmask_cont_hips.png'), cmask_cont_hips)
        cv2.imwrite(os.path.join(
            s_save, f'{num}_cmask_secr_inn.png'), cmask_secr_inn)
        cv2.imwrite(os.path.join(
            s_save, f'{num}_cmask_cont_inn.png'), cmask_cont_inn)
        
        # cv2.imshow('tmp', cmask_cont_inn)
        # cv2.waitKey(0)
