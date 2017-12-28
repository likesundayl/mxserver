# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from mxnet.image.image import ImageIter
from mxnet.io import DataBatch


def load_data_iter_rec(data_config_dict):
    target = data_config_dict['target']
    label_name = data_config_dict['label'][0]['label_name']
    label_width = int(data_config_dict['label'][0]['label_width'])
    data_name = data_config_dict['data_name_shapes'][0]['data_name']
    data_shapes = data_config_dict['data_name_shapes'][0]['shapes']
    data_shape_list = [int(data_shape) for data_shape in data_shapes]
    if target == 'train':
        train_config = data_config_dict['train_config']
        data_config = train_config['data_config']
        batch_size = int(data_config['batch_size'])
        if data_config['shuffle'] == '0':
            shuffle = True
        else:
            shuffle = False
        train_set_rec = data_config['train_set'][0]
        if len(data_config['train_set']) == 2:
            train_set_idx = data_config['train_set'][1]
        else:
            train_set_idx = None
        train_iter = ImageIter(batch_size=batch_size, data_shape=tuple(data_shape_list), label_width=label_width,
                               path_imgrec=train_set_rec, path_imgidx=train_set_idx, data_name=data_name,
                               shuffle=shuffle, label_name=label_name)
        if data_config.get('val_set') is None:
            return [train_iter]
        else:
            val_set_rec = data_config['val_set'][0]
            if len(data_config['val_set']) == 2:
                val_set_idx = data_config['val_set'][1]
            else:
                val_set_idx = None
            val_iter = ImageIter(batch_size=batch_size, data_shape=tuple(data_shape_list), label_width=label_width,
                                 path_imgrec=val_set_rec, path_imgidx=val_set_idx, data_name=data_name,
                                 shuffle=shuffle, label_name=label_name)
            return [train_iter, val_iter]
    else:
        test_config = data_config_dict['test_config']
        test_datas = test_config['data_config']['datas']
        # TODO:
        return None

