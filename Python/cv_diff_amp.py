import torch
import numpy as np
import cv2


def numpy2torch(img_np):
    img_torch = torch.from_numpy(img_np.astype(
        np.float32) / 255.0).permute(2, 0, 1).contiguous().unsqueeze(0)
    return img_torch


def tensor2img(tensor, out_type=np.uint8, min_max=(0, 1)):
    '''
    Converts a torch Tensor into an image Numpy array
    Input: 4D(B,(3/1),H,W), 3D(C,H,W), or 2D(H,W), any range, RGB channel order
    Output: 3D(H,W,C) or 2D(H,W), [0,255], np.uint8 (default)
    '''
    tensor = tensor.squeeze().float().cpu().clamp_(*min_max)  # clamp
    tensor = (tensor - min_max[0]) / \
        (min_max[1] - min_max[0])  # to range [0,1]
    n_dim = tensor.dim()

    if n_dim == 3:
        img_np = tensor.numpy()
        img_np = np.transpose(img_np[[2, 1, 0], :, :], (1, 2, 0))  # HWC, BGR
    elif n_dim == 2:
        img_np = tensor.numpy()
    else:
        raise TypeError(
            'Only support 4D, 3D and 2D tensor. But received with dimension: {:d}'.format(n_dim))
    if out_type == np.uint8:
        img_np = (img_np * 255.0).round()
        # Important. Unlike matlab, numpy.unit8() WILL NOT round by default.
    return img_np.astype(out_type)


def genDiff(cv_1, cv_2, amp=50):
    ten_1 = numpy2torch(cv_1)
    ten_2 = numpy2torch(cv_2)
    return tensor2img((ten_1 - ten_2)*amp)

if __name__ == "__main__":
    cv_rev = cv2.imread(
        '/home/zeit/SDB/NiseEngFolder/forTestModels/forMEDFE/result/901_mine_out_DE.png')
    cv_rev_gt = cv2.imread(
        '/home/zeit/SDB/NiseEngFolder/forTestModels/forMEDFE/result/901_official_out.png')
    cv_diff = genDiff(cv_rev, cv_rev_gt, 10)
    
    cv2.imshow('rev', cv_rev_gt)
    cv2.imshow('rev_gt', cv_rev_gt)
    cv2.imshow('diff', cv_diff)
    cv2.waitKey(0)
