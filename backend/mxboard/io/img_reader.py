# -*- coding: utf-8 -*-

# @Time    : 2018/1/3 16:16
# @Author  : Terence Wu
# @License : Copyright (c) Terence Wu
import cv2


def read_imgs(img_list):
    imgs = [cv2.imread(img) for img in img_list]
    return imgs

