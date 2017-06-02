from skimage import io, img_as_float
import numpy as np
import os
import ipre


def iip(imfile):
    cf_list = os.listdir("result")
    char_set = []
    char_img = []
    for each in cf_list:
        char_set.append(each.split(".")[0])
        temp_i = img_as_float(io.imread("result/" + each))
        char_img.append(temp_i)
    imf = io.imread(imfile)
    imf = ipre.mean_grey(imf)
    parts = ipre.im_cut(imf)
    res_str = ""
    for each in parts:
        max_idx = 0
        value = 0.0
        for i in range(len(char_img)):
            temp = np.sum(char_img[i] * each) / np.sqrt(np.sum(char_img[i] **
                                                               2.0))
            if temp > value:
                value = temp
                max_idx = i
        res_str += char_set[max_idx]
    return res_str
