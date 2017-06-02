import glob
import warnings
from skimage import io, img_as_float
import numpy as np
import os


def mean_grey(im_file):
    image = img_as_float(im_file)[10:48, 54:146, :]
    mg = np.mean(image)
    wt = np.ones_like(image)
    bk = np.zeros_like(image)
    out = np.where(image < mg, bk, wt)
    return out


def im_cut(out):
    return [out[:, 0:23, :], out[:, 23:46, :], out[:, 46:69, :], out[:, 69:, :]]


def im_classifier(each_part):
    response = input("Class: ")
    if response == "":
        return
    else:
        if not os.path.exists(str(response)):
            os.mkdir(str(response))
        num = str(len(os.listdir(str(response))))
        io.imsave(str(response) + "/" + num + ".png", each_part)
        return


if __name__ == "__main__":
    warnings.simplefilter("ignore")
    im_list = glob.glob("*.jpg")
    for each_jpg in im_list:
        imf = io.imread(each_jpg)
        imf = mean_grey(imf)
        parts = im_cut(imf)
        io.imshow(imf)
        io.show()
        for each in parts:
            im_classifier(each)
