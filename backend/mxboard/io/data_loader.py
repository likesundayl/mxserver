# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import cv2
import numpy as np
from mxnet import nd
from collections import namedtuple
from mxnet.image.image import ImageIter

Batch = namedtuple('Batch', ['data'])


def load_data(for_training, exec_type, data_config_dict):
    # TODO:
    pass


class ClsRecordIOCreator(object):
    def __init__(self, img_root, lst_path, rec_config):
        self._img_root = img_root
        self._lst_path = lst_path
        self._rec_config = rec_config

    def create(self):
        # TODO:
        pass


class ClsDataBatchLoader(object):
    def __init__(self, img_list, config):
        self._img_list = img_list
        self._img_shapes = [int(shape) for shape in config['img_shapes']]

    def load_data_batchs(self):
        data_batchs = {}

        for img in self._img_list:
            cv_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
            if cv_img is not None:
                cv_img = cv2.resize(cv_img, (self._img_shapes[0], self._img_shapes[1]))
                cv_img = np.swapaxes(cv_img, 0, 2)
                cv_img = np.swapaxes(cv_img, 1, 2)
                cv_img = cv_img[np.newaxis, :]
                data_batchs[img] = Batch([nd.array(cv_img)])

        return data_batchs


class DataIterCreator(object):
    def __init__(self):
        self._name = 'data_iter'

    def create(self):
        raise NotImplementedError()


class ClsDataIterCreator(DataIterCreator):
    def __init__(self, data_shape):
        super(ClsDataIterCreator, self).__init__()

    def create(self):
        pass


class DetecDataIterCreator(DataIterCreator):
    def __init__(self):
        super(DetecDataIterCreator, self).__init__()

    def create(self):
        pass
