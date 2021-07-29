from __future__ import print_function
import torch
import numpy as np
from PIL import Image
import random
import inspect, re
import numpy as np
import os
import collections
import math
import torch.nn.functional as F
from torch.autograd import Variable
import torch.nn as nn
from datetime import datetime
import logging
import cv2

# Converts a Tensor into a Numpy array
# |imtype|: the desired type of the converted numpy array
def tensor2im(image_tensor, imtype=np.uint8, neg=True):
    image_numpy = image_tensor[0].cpu().float().numpy()
    if image_numpy.shape[0] == 1:
        image_numpy = np.tile(image_numpy, (3,1,1))
    if neg:
        image_numpy = (np.transpose(image_numpy, (1, 2, 0)) + 1) / 2.0 * 255.0
    else:
        image_numpy = np.transpose(image_numpy, (1, 2, 0)) * 255.0
    return image_numpy.astype(imtype)


def diagnose_network(net, name='network'):
    mean = 0.0
    count = 0
    for param in net.parameters():
        if param.grad is not None:
            mean += torch.mean(torch.abs(param.grad.data))
            count += 1
    if count > 0:
        mean = mean / count
    print(name)
    print(mean)

def binary_mask(in_mask, threshold):
    assert in_mask.dim() == 2, "mask must be 2 dimensions"

    output = torch.ByteTensor(in_mask.size())
    output = (output > threshold).float().mul_(1)

    return output

def gussin(v):
    outk = []
    v = v
    for i in range(32):
        for k in range(32):

            out = []
            for x in range(32):
                row = []
                for y in range(32):
                    cord_x = i
                    cord_y = k
                    dis_x = np.abs(x - cord_x)
                    dis_y = np.abs(y - cord_y)
                    dis_add = -(dis_x * dis_x + dis_y * dis_y)
                    dis_add = dis_add / (2 * v * v)
                    dis_add = math.exp(dis_add) / (2 * math.pi * v * v)

                    row.append(dis_add)
                out.append(row)

            outk.append(out)

    out = np.array(outk)
    f = out.sum(-1).sum(-1)
    q = []
    for i in range(1024):
        g = out[i] / f[i]
        q.append(g)
    out = np.array(q)
    return torch.from_numpy(out)

def cal_feat_mask(inMask, nlayers):
    assert inMask.dim() == 4, "mask must be 4 dimensions"
    inMask = inMask.float()
    ntimes = 2**nlayers
    inMask = F.interpolate(inMask, (inMask.size(2)//ntimes, inMask.size(3)//ntimes), mode='nearest')
    inMask = inMask.detach().byte()

    return inMask

def cal_mask_given_mask_thred(img, mask, patch_size, stride, mask_thred):
    assert img.dim() == 3, 'img has to be 3 dimenison!'
    assert mask.dim() == 2, 'mask has to be 2 dimenison!'
    dim = img.dim()
    #math.floor 是向下取整
    _, H, W = img.size(dim-3), img.size(dim-2), img.size(dim-1)
    nH = int(math.floor((H-patch_size)/stride + 1))
    nW = int(math.floor((W-patch_size)/stride + 1))
    N = nH*nW

    flag = torch.zeros(N).long()
    offsets_tmp_vec = torch.zeros(N).long()
    #返回的是一个list类型的数据

    nonmask_point_idx_all = torch.zeros(N).long()

    tmp_non_mask_idx = 0


    mask_point_idx_all = torch.zeros(N).long()

    tmp_mask_idx = 0
    #所有的像素点都浏览一遍
    for i in range(N):
        h = int(math.floor(i/nW))
        w = int(math.floor(i%nW))
        # print(h, w)
        #截取一个个1×1的小方片
        mask_tmp = mask[h*stride:h*stride + patch_size,
                        w*stride:w*stride + patch_size]


        if torch.sum(mask_tmp) < mask_thred:
            nonmask_point_idx_all[tmp_non_mask_idx] = i
            tmp_non_mask_idx += 1
        else:
            mask_point_idx_all[tmp_mask_idx] = i
            tmp_mask_idx += 1
            flag[i] = 1
            offsets_tmp_vec[i] = -1
    # print(flag)  #checked
    # print(offsets_tmp_vec) # checked

    non_mask_num = tmp_non_mask_idx
    mask_num = tmp_mask_idx

    nonmask_point_idx = nonmask_point_idx_all.narrow(0, 0, non_mask_num)
    mask_point_idx=mask_point_idx_all.narrow(0, 0, mask_num)

    # get flatten_offsets
    flatten_offsets_all = torch.LongTensor(N).zero_()
    for i in range(N):
        offset_value = torch.sum(offsets_tmp_vec[0:i+1])
        if flag[i] == 1:
            offset_value = offset_value + 1
        # print(i+offset_value)
        flatten_offsets_all[i+offset_value] = -offset_value

    flatten_offsets = flatten_offsets_all.narrow(0, 0, non_mask_num)

    # print('flatten_offsets')
    # print(flatten_offsets)   # checked


    # print('nonmask_point_idx')
    # print(nonmask_point_idx)  #checked

    return flag, nonmask_point_idx, flatten_offsets, mask_point_idx


# sp_x: LongTensor
# sp_y: LongTensor
def cal_sps_for_Advanced_Indexing(h, w):
    sp_y = torch.arange(0, w).long()
    sp_y = torch.cat([sp_y]*h)

    lst = []
    for i in range(h):
        lst.extend([i]*w)
    sp_x = torch.from_numpy(np.array(lst))
    return sp_x, sp_y


def save_image(image_numpy, image_path):
    image_pil = Image.fromarray(image_numpy)
    image_pil.save(image_path)

def info(object, spacing=10, collapse=1):
    """Print methods and doc strings.
    Takes module, class, list, dictionary, or string."""
    methodList = [e for e in dir(object) if isinstance(getattr(object, e), collections.Callable)]
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print( "\n".join(["%s %s" %
                     (method.ljust(spacing),
                      processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList]) )

def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
            return m.group(1)

def print_numpy(x, val=True, shp=False):
    x = x.astype(np.float64)
    if shp:
        print('shape,', x.shape)
    if val:
        x = x.flatten()
        print('mean = %3.3f, min = %3.3f, max = %3.3f, median = %3.3f, std=%3.3f' % (
            np.mean(x), np.min(x), np.max(x), np.median(x), np.std(x)))


def mkdirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        
        
# ==============================================
#           Borrowed From Others
# ==============================================

def get_timestamp():
    return datetime.now().strftime('%y%m%d-%H%M%S')


def setup_logger(logger_name, root, phase, level=logging.INFO, screen=False, tofile=False):
    '''set up logger'''
    lg = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s',
                                  datefmt='%y-%m-%d %H:%M:%S')
    lg.setLevel(level)
    if tofile:
        log_file = os.path.join(
            root, phase + '_{}.log'.format(get_timestamp()))
        fh = logging.FileHandler(log_file, mode='w')
        fh.setFormatter(formatter)
        lg.addHandler(fh)
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        lg.addHandler(sh)

# ----------------------------------
#           for metric

def bgr2ycbcr(img, only_y=True):
    '''bgr version of rgb2ycbcr
    only_y: only return Y channel
    Input:
        uint8, [0, 255]
        float, [0, 1]
    '''
    in_img_type = img.dtype
    img.astype(np.float32)
    if in_img_type != np.uint8:
        img *= 255.
    # convert
    if only_y:
        rlt = np.dot(img, [24.966, 128.553, 65.481]) / 255.0 + 16.0
    else:
        rlt = np.matmul(img, [[24.966, 112.0, -18.214], [128.553, -74.203, -93.786],
                              [65.481, -37.797, 112.0]]) / 255.0 + [16, 128, 128]
    if in_img_type == np.uint8:
        rlt = rlt.round()
    else:
        rlt /= 255.
    return rlt.astype(in_img_type)


def calculate_psnr(img1, img2):
    # img1 and img2 have range [0, 255]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))


def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')
