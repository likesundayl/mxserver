# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import sys
from os import path as osp
from backend.mxboard.util.xml_parser import mxboard_mxnet_config
from backend.mxboard.util.task_desc_parser import generate_initializer, generate_lr_scheduler
from mxnet.module import Module
from mxnet import nd
from mxnet import sym
from backend.mxboard.util.xml_parser import mxboard_storage_config

params_root_path = mxboard_storage_config['params-root']

RCNN_PATH = mxboard_mxnet_config['rcnn-path']
sys.path.append(RCNN_PATH)


class Executor(object):
    def __init__(self):
        self._mod = None

    def execute(self):
        pass

    @staticmethod
    def load_check_point(sym_json_path, params_path):
        symbol = sym.load(sym_json_path)
        save_dict = nd.load(params_path)
        arg_params = {}
        aux_params = {}
        for k, v in save_dict.items():
            tp, name = k.split(':', 1)
            if tp == 'arg':
                arg_params[name] = v
            if tp == 'aux':
                aux_params[name] = v
        mod = Module(symbol=symbol)
        mod._arg_params = arg_params
        mod._aux_params = aux_params
        mod.params_initialized = True
        # TODO: There is a parameter named load_optimizer_states in Module.load
        return mod

    @staticmethod
    def create_executor(for_training, exec_type, **kwargs):
        if for_training:
            if exec_type == 'classify':
                return Executor._registered_trainer['classifytrainer'](**kwargs)
            elif exec_type == 'detection':
                return Executor._registered_trainer['rcnntrainer'](**kwargs)
        else:
            if exec_type == 'classify':
                return Executor._registered_predictor['classifier'](**kwargs)
            elif exec_type == 'detection':
                return Executor._registered_trainer['objectdetector'](**kwargs)

    _registered_predictor = {}
    _registered_trainer = {}

    @staticmethod
    def register(kclass, for_training):
        assert (isinstance(kclass, type))
        name = kclass.__name__.lower()
        if for_training:
            if name not in Executor._registered_trainer:
                Executor._registered_trainer[name] = kclass
        else:
            if name not in Executor._registered_predictor:
                Executor._registered_predictor[name] = kclass
        return kclass


register = Executor.register


class Predictor(Executor):
    def __init__(self, sym_json_path, params_path):
        super(Predictor, self).__init__()
        self._mod = Executor.load_check_point(sym_json_path=sym_json_path, params_path=params_path)


@register(for_training=False)
class Classifier(Predictor):
    def __init__(self, sym_json_path, params_path):
        super(Classifier, self).__init__(sym_json_path=sym_json_path, params_path=params_path)
        pass


@register(for_training=False)
class ObjectDetector(Predictor):
    def __init__(self, sym_json_path, params_path):
        super(ObjectDetector, self).__init__(sym_json_path=sym_json_path, params_path=params_path)


class Trainer(Executor):
    def __init__(self, sym, init_config, lr_config, opt_config):
        super(Trainer, self).__init__()

    @staticmethod
    def _prepare_initializer(init_config):
        return generate_initializer(init_config)

    @staticmethod
    def _prepare_optimizer(opt_config):
        mxnet_opt_params = {}
        opt_params = opt_config['opt_config']
        for key, value in opt_params.iteritems():
            if value.isdigit():
                mxnet_opt_params[key] = float(value)
            elif value == 'true':
                mxnet_opt_params[key] = True
            elif value == 'false':
                mxnet_opt_params[key] = False
            else:
                mxnet_opt_params[key] = value
        return opt_config['type'], mxnet_opt_params

    @staticmethod
    def _prepare_lr_scheduler(lr_config):
        return generate_lr_scheduler(lr_config)


@register(for_training=True)
class ClassifyTrainer(Trainer):
    def __init__(self, symbol, data_names, label_names, init_config, lr_config, opt_config, resume_config):
        super(ClassifyTrainer, self).__init__(symbol, init_config, lr_config, opt_config)
        self._mod = ClassifyTrainer._prepare_module(symbol=symbol, data_names=data_names, label_names=label_names,
                                                    resume_config=resume_config)

    @staticmethod
    def _prepare_module(symbol, data_names, label_names, resume_config):
        if not resume_config['is_resume'] == '0':
            return Module(symbol=symbol, data_names=data_names, label_names=label_names)
        else:
            ckp = resume_config['ckp']
            prefix = ckp['prefix']
            epoch = ckp['epoch']
            params_path = osp.join(params_root_path, '%s-%04d.params' % (prefix, epoch))
            save_dict = nd.load(params_path)
            arg_params = {}
            aux_params = {}
            for k, v in save_dict.items():
                tp, name = k.split(':', 1)
                if tp == 'arg':
                    arg_params[name] = v
                if tp == 'aux':
                    aux_params[name] = v
            mod = Module(symbol=symbol)
            mod._arg_params = arg_params
            mod._aux_params = aux_params
            mod.params_initialized = True
            # TODO: There is a parameter named load_optimizer_states in Module.load
            return mod


@register(for_training=True)
class RCNNTrainer(Trainer):
    def __init__(self, symbol, data_names, label_names, init_config, lr_config, opt_config, resume_config):
        super(RCNNTrainer, self).__init__(symbol, init_config, lr_config, opt_config)
        pass

    @staticmethod
    def _prepare_module(symbol, resume_config):
        # TODO:
        pass
