# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 28/02/18 上午 11:35

# MXNet's License(Copy some codes from the original mxnet/example/rcnn)
from os.path import join
from config import MXSERVER_HOME

import numpy as np


class IMDB(object):
    def __init__(self, name):
        self._name = name
        self._cache_path = join(MXSERVER_HOME, 'rcnn_cache')

        self.classes = []
        self.num_classes = 0
        self.image_set_index = []
        self.num_images = 0

        self.config = {}

    @staticmethod
    def merge_roidbs(a, b):
        """
        Copyed from original mxnet
        merge roidbs into one
        :param a: roidb to be merged into
        :param b: roidb to be merged
        :return: merged imdb
        """
        assert len(a) == len(b)
        for i in range(len(a)):
            a[i]['boxes'] = np.vstack((a[i]['boxes'], b[i]['boxes']))
            a[i]['gt_classes'] = np.hstack((a[i]['gt_classes'], b[i]['gt_classes']))
            a[i]['gt_overlaps'] = np.vstack((a[i]['gt_overlaps'], b[i]['gt_overlaps']))
            a[i]['max_classes'] = np.hstack((a[i]['max_classes'], b[i]['max_classes']))
            a[i]['max_overlaps'] = np.hstack((a[i]['max_overlaps'], b[i]['max_overlaps']))
        return a