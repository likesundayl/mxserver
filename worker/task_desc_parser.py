# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import json
import os.path as osp

from mxnet import symbol as sym, initializer as init, lr_scheduler as ls, Context

from util.conf_parser import mxserver_storage_config
from worker.mxnet_extension.core.model_zoo.model_factory import get_symbol

symbol_root_path = mxserver_storage_config['symbol-json-root']
params_root_path = mxserver_storage_config['params-root']


def parse_task_desc(task_desc):
    task_dict = json.loads(task_desc)

    executor_params_dict = dict()

    executor_params_dict['classes'] = [class_name for class_name in task_desc['classes']]

    ##########################################
    # Prepare net
    ##########################################
    net_dict = task_dict['net']
    net_type = net_dict['type']
    net_name = net_dict['name']

    if net_type == 'built_in':
        net_config = net_dict['config']
        executor_params_dict['sym_json_path'] = get_symbol(name=net_name, config=net_config)
    else:
        # TODO: What if there is no such file?
        executor_params_dict['sym_json_path'] = osp.join(symbol_root_path, net_name)

    for_training = True
    if task_dict['for_training'] == '1':
        for_training = False

    exec_type = task_dict['target']

    # eval metrics
    eval_metrics = tuple(task_dict['eval_metrics'])
    if len(eval_metrics) == 0:
        executor_params_dict['eval_metrics'] = None
    else:
        executor_params_dict['eval_metrics'] = eval_metrics

    if for_training:
        # If for training, then get the symbol
        executor_params_dict['symbol'] = sym.load(osp.join(symbol_root_path, net_name))

        train_config = task_dict['train_param']

        # data names and label names
        data_config = train_config['data_param']
        label_config = train_config['label_param']
        executor_params_dict['data_names'] = tuple(data_config['name'])
        executor_params_dict['label_names'] = tuple(label_config['name'])

        # context
        executor_params_dict['ctx_config'] = task_dict['context']

        # initializer
        executor_params_dict['init_config'] = train_config['initializer']

        # optimizer
        executor_params_dict['opt_config'] = train_config['optimizer']

        # lr scheduler
        executor_params_dict['lr_config'] = train_config['lr_scheduler']

        # resume config
        executor_params_dict['resume_config'] = train_config['resume_config']
    else:
        test_param = task_dict['test_param']
        ckp = test_param['ckp']
        executor_params_dict['params_path'] = osp.join(params_root_path, '%s-%04d.params' % (ckp['prefix'], int(ckp['epoch'])))
        test_label_config = test_param['label']
        executor_params_dict['label'] = None
        if exec_type == 'classify':
            if test_label_config.get('cls_label') is not None:
                executor_params_dict['label'] = test_label_config['cls_label']
        elif exec_type == 'detection':
            if test_label_config.get('detec_xml_label') is not None:
                executor_params_dict['label'] = test_label_config['detec_xml_label']

    return for_training, exec_type, executor_params_dict


def get_data_config(task_desc):
    task_dict = json.loads(task_desc)
    if task_dict['for_training'] == '0':
        data_config = task_dict['train_param']['data_param']
    else:
        data_config = task_dict['test_param']['test_img_config']
    return data_config


def generate_ctx(ctx_config):
    ctx_list = []

    for ctx in ctx_config:
        name = ctx['device_name']
        if name == 'cpu':
            ctx_list.append(Context(device_type=name, device_id=0))
            return ctx_list
        else:
            device_id = int(ctx['device_id'])
            ctx_list.append(Context(device_type='gpu', device_id=device_id))
    return tuple(ctx_list)


def generate_initializer(init_dict):
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


def generate_lr_scheduler(ls_dict):
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

