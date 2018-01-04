# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import sys
from backend.mxboard.util.xml_parser import mxboard_mxnet_config
from mxnet.module import Module

RCNN_PATH = mxboard_mxnet_config['rcnn-path']
sys.path.append(RCNN_PATH)


class Executor(Module):
    def __init__(self, symbol, data_iters, ctx_list, initializer, lr_scheduler, optimizer, data_names, label_names):
        super(Executor, self).__init__(symbol=symbol, data_names=data_names, label_names=label_names, logger=None,
                                       context=ctx_list, work_load_list=None, fixed_param_names=None, state_names=None)
        self._train_iter = data_iters[0]
        if len(data_iters) == 2:
            self._val_iter = data_iters[1]
        else:
            self._val_iter = None

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
    def __init__(self):
        pass


@register(for_training=False)
class Classifier(Predictor):
    def __init__(self):
        pass


@register(for_training=False)
class ObjectDetector(Predictor):
    def __init__(self):
        pass


class Trainer(Executor):
    def __init__(self):
        pass


@register(for_training=True)
class ClassifyTrainer(Trainer):
    def __init__(self):
        pass


@register(for_training=True)
class RCNNTrainer(Trainer):
    def __init__(self):
        pass
