# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import json
import os.path as osp
from mxnet import symbol as sym, initializer as init, lr_scheduler as ls, Context
from backend.mxboard.util.xml_parser import mxboard_storage_config

symbol_root_path = mxboard_storage_config['symbol-json-root']


def parse_task_desc(task_desc):
    task_dict = json.loads(task_desc)

    #############################################################
    # Prepare net
    #############################################################
    net_name = task_dict['net']
    net_full_path = osp.join(symbol_root_path, net_name + '.json')
    net_symbol = sym.load(net_full_path)

    #############################################################
    # Prepare ctx
    #############################################################
    ctx_config = task_dict['ctx']
    ctx_list = _generate_ctx(ctx_config)

    #############################################################
    # Prepare data(including data and label config)
    #############################################################
    data_dict = task_dict['data']

    #############################################################
    # Prepare initializer
    #############################################################
    init_dict = task_dict['initializer']
    initializer = _generate_initializer(init_dict)

    #############################################################
    # Prepare lr_scheduler
    #############################################################
    ls_dict = task_dict['lr_scheduler']
    lr_scheduler = _generate_lr_scheduler(ls_dict)

    #############################################################
    # Prepare optimizer
    #############################################################
    opt_dict = task_dict['optimizer']
    optimizer = _generate_optimizer(opt_dict)

    return net_symbol, ctx_list, data_dict, initializer, lr_scheduler, optimizer


def get_data_and_label_names(data_config_dict):
    label_config = data_config_dict['label']
    label_names = [label['label_name'] for label in label_config]
    data_config = data_config_dict['data_name_shapes']
    data_names = [data['data_name'] for data in data_config]
    return data_names, label_names


def _generate_ctx(ctx_config):
    ctx_list = []

    for ctx in ctx_config:
        name = ctx['device_name']
        if name == 'cpu':
            ctx_list.append(Context(device_type=name, device_id=0))
            return ctx_list
        else:
            device_id = int(ctx['device_id'])
            ctx_list.append(Context(device_type='gpu', device_id=device_id))
    return ctx_list


def _generate_initializer(init_dict):
    init_type = init_dict['type']
    init_param = init_dict['param']

    # currently Uniform, Normal, Xavier, MSRAPrelu are supported
    if init_type == 'Uniform':
        scale = float(init_param['scale'])
        return init.Uniform(scale)
    if init_type == 'Normal':
        sigma = float(init_param['sigma'])
        return init.Normal(sigma)
    # Xavier
    if init_type == 'Xavier':
        magnitude = float(init_param['magnitude'])
        return init.Xavier(magnitude=magnitude)
    # PReLU
    if init_type == 'MSRAPrelu':
        slope = float(init_param['slope'])
        return init.MSRAPrelu(factor_type='avg', slope=slope)


def _generate_lr_scheduler(ls_dict):
    scheduler_type = ls_dict['type']
    scheduler_param = ls_dict['param']
    # currently just return a FactorScheduler
    if scheduler_type == 'Factor':
        step = int(scheduler_param['step'])
        factor = float(scheduler_param['factor'])
        stop_factor_lr = float(scheduler_param['stop_factor_lr'])
        return ls.FactorScheduler(step, factor, stop_factor_lr)


def _generate_optimizer(opt_dict):
    op_type = opt_dict['type'].lower()
    kvstore = opt_dict['kvstore']
    op_param = opt_dict['param']
    base_lr = float(op_param['base_lr'])
    momentum = float(op_param['momentum'])
    weight_decay = float(op_param['weight_decay'])

    op_param_tuple = (op_type, kvstore, (base_lr, momentum, weight_decay))
    return op_param_tuple
