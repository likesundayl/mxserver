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
            val_rec = file_path.get('val_rec')
            data_iter_creator = ClsDataIterCreator(train_rec_path=train_rec, batch_size=batch_size,
                                                   data_shape=data_shapes, shuffle=shuffle, train_idx_path=train_idx,
                                                   val_rec_path=val_rec)
            return data_iter_creator.create()
        elif exec_type == 'detection':
            # TODO: It seems that I have to understanding codes in mxnet_extension/example/rcnn
            pass
    else:
        img_list = data_config_dict['img_list']
        label = True
        if len(data_config_dict['label']) == 0:
            label = False

        if exec_type == 'classify':
            if label:
                img_label_txt = data_config_dict['label']['cls_label']
            else:
                img_label_txt = None
            loader = ClsDataBatchLoader(img_list=img_list, config=data_config_dict,
                                        img_label_txt=img_label_txt)
            return loader.load_data_batchs()
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
    def __init__(self, img_list, config, img_label_txt=None):
        self._img_list = img_list
        self._img_shapes = [int(shape) for shape in config['img_shapes']]
        self._img_label_txt = img_label_txt

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

        if self._img_label_txt:
            label_dict = {}
            cls_label = open(self._img_label_txt, 'r')
            line = cls_label.readline()
            while line:
                contents = line.split('\t')
                img_name = contents[0]
                img_label = int(contents[1])
                label_dict[img_name] = img_label
                line = cls_label.readline()
            return data_batchs, label_dict
        else:
            return data_batchs


class DataIterCreator(object):
    def __init__(self):
        self._name = 'data_iter'

    def create(self):
        raise NotImplementedError()


class ClsDataIterCreator(DataIterCreator):
    def __init__(self, train_rec_path, batch_size, data_shape, shuffle=False, train_idx_path=None, val_rec_path=None):
        super(ClsDataIterCreator, self).__init__()
        self._train_rec_path = train_rec_path
        self._batch_size = batch_size
        self._data_shape = data_shape
        self._shuffle = shuffle
        self._train_idx_path = train_idx_path
        self._val_rec_path = val_rec_path

    def create(self):
        if self._train_idx_path is None:
            self._shuffle = False
        train_iter = ImageIter(batch_size=self._batch_size, data_shape=self._data_shape, shuffle=self._shuffle,
                               path_imgrec=self._train_rec_path, path_imgidx=self._train_idx_path)
        if self._val_rec_path is None:
            return train_iter
        else:
            val_iter = ImageIter(batch_size=self._batch_size, data_shape=self._data_shape, shuffle=False,
                                 path_imgrec=self._val_rec_path)
            return train_iter, val_iter


class DetecDataIterCreator(DataIterCreator):
    def __init__(self):
        super(DetecDataIterCreator, self).__init__()

    def create(self):
        pass

