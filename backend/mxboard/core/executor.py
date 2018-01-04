# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import sys
from backend.mxboard.util.xml_parser import mxboard_mxnet_config
from mxnet.module import Module
from mxnet import nd
from mxnet import sym

RCNN_PATH = mxboard_mxnet_config['rcnn-path']
sys.path.append(RCNN_PATH)


class Executor(object):
    def __init__(self):
        self._mod = None

    def execute(self):
        pass

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
        self._mod = Predictor.load_check_point(sym_json_path=sym_json_path, params_path=params_path)

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
    def __init__(self):
        super(Trainer, self).__init__()
        pass


@register(for_training=True)
class ClassifyTrainer(Trainer):
    def __init__(self):
        super(ClassifyTrainer, self).__init__()
        pass


@register(for_training=True)
class RCNNTrainer(Trainer):
    def __init__(self):
        super(RCNNTrainer, self).__init__()
        pass
