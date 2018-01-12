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
    if for_training:
        if exec_type == 'classify':
            batch_size = int(data_config_dict['batch_size'])
            data_shapes = tuple([int(shape) for shape in data_config_dict['shapes']])
            if data_config_dict['shuffle'] == '0':
                shuffle = True
            else:
                shuffle = False
            file_path = data_config_dict['file_path']
            train_rec = file_path['train_rec']
            if shuffle:
                train_idx = file_path.get('train_idx')
                if train_idx is None:
                    shuffle = False
            train_iter = ImageIter(batch_size=batch_size, data_shape=data_shapes, shuffle=shuffle,
                                   path_imgrec=train_rec, path_imgidx=train_idx)
            val_rec = file_path.get('val_rec')
            if val_rec is None:
                return tuple(train_iter)
            else:
                val_iter = ImageIter(batch_size=batch_size, data_shape=data_shapes, shuffle=False, path_imgrec=val_rec)
                return train_iter, val_iter
            # TODO: To finish this part by ClsDataIterCreator in the future
        elif exec_type == 'detection':
            # TODO: It seems that I have to understanding codes in mxnet/example/rcnn
            pass
    else:
        img_list = data_config_dict['img_list']
        label = True
        if len(data_config_dict['label']) == 0:
            label = False
        if label:
            # If correct label is provided
            pass
        else:
            # If correct label is not provided, then just generate the data batch
            if exec_type == 'classify':
                data_batchs = {}
                img_shape = [int(shape) for shape in data_config_dict['img_shapes']]

                for img in img_list:
                    cv_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
                    if cv_img is not None:
                        cv_img = cv2.resize(cv_img, (img_shape[0], img_shape[1]))
                        cv_img = np.swapaxes(cv_img, 0, 2)
                        cv_img = np.swapaxes(cv_img, 1, 2)
                        cv_img = cv_img[np.newaxis, :]
                        data_batchs[img] = Batch([nd.array(cv_img)])

                return data_batchs
                # TODO: To finish this part by ClsDataBatchLoader in the future
            elif exec_type == 'detection':
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

