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
        elif exec_type == 'detection':
            # TODO:
            pass
    else:
        test_datas = {}
        img_list = data_config_dict['img_list']
        img_shape = [int(shape) for shape in data_config_dict['img_shapes']]

        for img in img_list:
            cv_img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2RGB)
            if img is not None:
                cv_img = cv2.resize(cv_img, (img_shape[0], img_shape[1]))
                cv_img = np.swapaxes(cv_img, 0, 2)
                cv_img = np.swapaxes(cv_img, 1, 2)
                cv_img = cv_img[np.newaxis, :]
            test_datas[img] = Batch([nd.array(cv_img)])

        return test_datas
