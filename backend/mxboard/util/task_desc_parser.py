# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import json
import os.path as osp
from mxnet import symbol as sym, initializer as init, lr_scheduler as ls, Context
from backend.mxboard.util.xml_parser import mxboard_storage_config

symbol_root_path = mxboard_storage_config['symbol-json-root']
params_root_path = mxboard_storage_config['params-root']


def parse_task_desc(task_desc):
    task_dict = json.loads(task_desc)

    ##########################################
    # Prepare net
    ##########################################
    net_dict = task_dict['net']
    net_name = net_dict['name']
    # TODO: What if there is no such file?
    net_symbol_json_path = osp.join(symbol_root_path, net_name)

    for_training = True
    if task_dict['for_training'] == '1':
        for_training = False

    exec_type = task_dict['target']
    executor_dict = {}

    if task_dict['for_training'] == '0':
        # If for training, then get the symbol
        executor_dict['symbol'] = sym.load(net_symbol_json_path)
        executor_dict['train_config'] = task_dict['train_param']
    else:
        test_param = task_dict['test_param']
        ckp = test_param['ckp']
        executor_dict['sym_json_path'] = net_symbol_json_path
        executor_dict['params_path'] = osp.join(params_root_path, '%s-%04d.params' % (ckp['prefix'], int(ckp['epoch'])))

    return for_training, exec_type, executor_dict


def get_data_config(task_desc):
    task_dict = json.loads(task_desc)
    if task_dict['for_training'] == '0':
        data_config = task_dict['train_param']['data_param']
    else:
        data_config = task_dict['test_param']['test_imgs']
    return data_config


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
    init_param = init_dict['init_config']

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
    scheduler_param = ls_dict['lr_scheduler_config']
    factor = float(scheduler_param['factor'])
    if scheduler_type == 'Factor':
        step = int(scheduler_param['step'])
        stop_factor_lr = float(scheduler_param['stop_factor_lr'])
        return ls.FactorScheduler(step, factor, stop_factor_lr)
    elif scheduler_type == 'MultiFactor':
        steps = scheduler_param['steps']
        step_list = [int(step) for step in steps]
        return ls.MultiFactorScheduler(step=step_list, factor=factor)


def _generate_optimizer(opt_dict):
    op_type = opt_dict['type'].lower()
    kvstore = opt_dict['kvstore']
    op_param = opt_dict['opt_config']
    base_lr = float(op_param['base_lr'])
    momentum = float(op_param['momentum'])
    weight_decay = float(op_param['weight_decay'])

    op_param_tuple = (op_type, kvstore, (base_lr, momentum, weight_decay))
    return op_param_tuple
