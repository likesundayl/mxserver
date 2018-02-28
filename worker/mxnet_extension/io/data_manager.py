# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 28/02/18 下午 02:01
from cv2 import imread, resize, cvtColor, COLOR_BGR2RGB
from os.path import exists, join
from os import sep
from urllib import urlretrieve
from shutil import copy
import numpy as np
from mxnet import nd
from collections import namedtuple
from mxnet.image.image import ImageIter

from util.conf_parser import mxserver_storage_config

Batch = namedtuple('Batch', ['data'])


class DataManager(object):
    def __init__(self, for_training, target, data_config):
        self._for_training = for_training
        self._target = target
        self._data_config = data_config

    def prepare_data(self):
        if self._for_training:
            if self._target == 'classify':
                batch_size = int(self._data_config['batch_size'])
                data_shapes = tuple([int(shape) for shape in self._data_config['shapes']])

                if self._data_config['shuffle'] == '0':
                    shuffle = True
                else:
                    shuffle = False

                train_rec = self._data_config['file_url'].get('train_rec')
                train_idx = self._data_config['file_url'].get('train_idx')
                val_rec = self._data_config['file_url'].get('val_rec')

                if self._data_config['source'] == 'internet':
                    # TODO, there is a problem
                    # train_rec
                    if train_rec is None:
                        raise ValueError('Field: train_rec\'s value must exists!')
                    train_rec_name = train_rec.split('/')[-1]
                    train_rec_path = join(mxserver_storage_config['data_center'], train_rec_name)
                    urlretrieve(train_rec, filename=train_rec_path)
                    train_rec = train_rec_path

                    # train_idx
                    if train_idx is not None:
                        train_idx_name = train_idx.split('/')[-1]
                        train_idx_path = join(mxserver_storage_config['data_center'], train_idx_name)
                        urlretrieve(train_idx, filename=train_idx_path)
                        train_idx = train_idx_path

                    # val_rec
                    if val_rec is not None:
                        val_rec_name = val_rec.split('/')[-1]
                        val_rec_path = join(mxserver_storage_config['data_center'], val_rec_name)
                        urlretrieve(val_rec, filename=val_rec_path)
                        val_rec = val_rec_path
                else:
                    # train_rec
                    if train_rec is None:
                        raise ValueError('Field: train_rec\'s value must exists!')
                    train_rec_name = train_rec.split(sep)[-1]
                    if not exists(train_rec):
                        raise IOError('Failed to find %s in local file system!' % train_rec)
                    if not exists(join(mxserver_storage_config['data_center'], train_rec_name)):
                        copy(train_rec, join(mxserver_storage_config['data_center'], train_rec_name))

                    # train_idx
                    if train_idx is not None:
                        train_idx_name = train_idx.split(sep)[-1]
                        if not exists(train_idx):
                            raise IOError('Failed to find %s in local file system!' % train_idx)
                        if not exists(join(mxserver_storage_config['data_center'], train_idx_name)):
                            copy(train_idx, join(mxserver_storage_config['data_center'], train_idx_name))

                    # val_rec
                    if val_rec is not None:
                        val_rec_name = val_rec.split(sep)[-1]
                        if not exists(val_rec):
                            raise IOError('Failed to find %s in local file system!' % val_rec)
                        if not exists(join(mxserver_storage_config['data_center'], val_rec_name)):
                            copy(val_rec, join(mxserver_storage_config['data_center'], val_rec_name))

                creator = ClsDataIterCreator(train_rec_path=train_rec, batch_size=batch_size,
                                             shuffle=shuffle, train_idx_path=train_idx, data_shape=data_shapes,
                                             val_rec_path=val_rec)
                return creator.create()
            elif self._target == 'detection':
                # TODO:
                pass
        else:
            if self._target == 'classify':
                if self._data_config['use_label'] == '1':
                    pass


class ClsDataBatchLoader(object):
    """
    Load DataBatch for classification
    """
    def __init__(self, img_list, config):
        self._img_list = img_list
        self._img_shapes = [int(shape) for shape in config['img_shapes']]

    def load_data_batchs(self):
        data_batchs = {}

        for img in self._img_list:
            cv_img = cvtColor(imread(img), COLOR_BGR2RGB)
            if cv_img is not None:
                cv_img = resize(cv_img, (self._img_shapes[0], self._img_shapes[1]))
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
