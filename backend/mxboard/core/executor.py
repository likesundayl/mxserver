# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import sys
from os import path as osp
from backend.mxboard.util.xml_parser import mxboard_mxnet_config
from backend.mxboard.util.task_desc_parser import generate_ctx, generate_initializer, generate_lr_scheduler
from backend.mxboard.core.callback import do_checkpoint
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
    def _prepare_ctx(ctx_config):
        return generate_ctx(ctx_config)

    @staticmethod
    def load_check_point(sym_json_path, params_path, ctx_config_tuple):
        ctx_config = list(ctx_config_tuple)
        # Copyed from MXNet

        # Licensed to the Apache Software Foundation (ASF) under one
        # or more contributor license agreements.  See the NOTICE file
        # distributed with this work for additional information
        # regarding copyright ownership.  The ASF licenses this file
        # to you under the Apache License, Version 2.0 (the
        # "License"); you may not use this file except in compliance
        # with the License.  You may obtain a copy of the License at
        #
        #   http://www.apache.org/licenses/LICENSE-2.0
        #
        # Unless required by applicable law or agreed to in writing,
        # software distributed under the License is distributed on an
        # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
        # KIND, either express or implied.  See the License for the
        # specific language governing permissions and limitations
        # under the License.
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
        mod = Module(symbol=symbol, context=generate_ctx(ctx_config), logger=None)
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
    def __init__(self, sym_json_path, params_path, ctx_config=({"device_name": "gpu", "device_id": "0"},)):
        super(Predictor, self).__init__()
        self._mod = Executor.load_check_point(sym_json_path=sym_json_path, params_path=params_path,
                                              ctx_config_tuple=ctx_config)

    def _predict(self):
        pass

    def execute(self):
        self._predict()


@register(for_training=False)
class Classifier(Predictor):
    def __init__(self, sym_json_path, params_path):
        super(Classifier, self).__init__(sym_json_path=sym_json_path, params_path=params_path)
        pass

    def _predict(self):
        pass


@register(for_training=False)
class ObjectDetector(Predictor):
    def __init__(self, sym_json_path, params_path):
        super(ObjectDetector, self).__init__(sym_json_path=sym_json_path, params_path=params_path)

    def _predict(self):
        pass


class Trainer(Executor):
    def __init__(self, train_iter, init_config, lr_config, opt_config, save_prefix, save_period, val_iter=None,
                 eval_metrics=('acc',), begin_epoch=0, num_epoch=250, kvstore='local'):
        super(Trainer, self).__init__()
        self._initializer = Trainer._prepare_initializer(init_config)
        self._lr_scheduler = Trainer._prepare_lr_scheduler(lr_config)
        self._opt_type, self._mxnet_opt_params = Trainer._prepare_optimizer(opt_config)
        self._train_iter = train_iter
        self._val_iter = val_iter
        self._save_prefix = save_prefix
        self._save_period = save_period
        self._eval_metrics = list(eval_metrics)
        self._begin_epoch = begin_epoch
        self._num_epoch = num_epoch
        self._kvstore = kvstore

    def _train(self):
        if not self._mod.params_initialized:
            self._mod.init_params(self._initializer, arg_params=None, aux_params=None, allow_missing=False,
                                  force_init=False)
        self._mod.init_optimizer(kvstore='local', optimizer=self._opt_type, optimizer_params=self._mxnet_opt_params,
                                 force_init=False)
        batch_end_callbacks = [

        ]
        epoch_end_callbacks = [
            do_checkpoint(self._save_prefix, self._save_period)
        ]
        self._mod.fit(train_data=self._train_iter,
                      eval_data=self._val_iter,
                      eval_metric=self._eval_metrics,
                      begin_epoch=self._begin_epoch,
                      num_epoch=self._num_epoch,
                      optimizer=self._opt_type,
                      optimizer_params=self._mxnet_opt_params,
                      initializer=self._initializer,
                      arg_params=self._mod.arg_params,
                      aux_params=self._mod.aux_paramsarams,
                      batch_end_callback=batch_end_callbacks,
                      epoch_end_callback=epoch_end_callbacks,
                      kvstore=self._kvstore,
                      allow_missing=True)

    def execute(self):
        self._train()

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
    def __init__(self, symbol, train_iter, ctx_config, data_names, label_names, init_config, lr_config, opt_config,
                 resume_config, val_iter=None):
        super(ClassifyTrainer, self).__init__(train_iter, init_config, lr_config, opt_config, val_iter=val_iter)
        self._mod = ClassifyTrainer._prepare_module(symbol=symbol, ctx_config=ctx_config, data_names=data_names,
                                                    label_names=label_names, resume_config=resume_config)

    @staticmethod
    def _prepare_module(symbol, ctx_config, data_names, label_names, resume_config):
        if not resume_config['is_resume'] == '0':
            return Module(symbol=symbol, context=Executor._prepare_ctx(ctx_config), data_names=data_names,
                          label_names=label_names)
        else:
            ckp = resume_config['ckp']
            prefix = ckp['prefix']
            epoch = ckp['epoch']
            params_path = osp.join(params_root_path, '%s-%04d.params' % (prefix, epoch))
            # Copyed from MXNet

            # Licensed to the Apache Software Foundation (ASF) under one
            # or more contributor license agreements.  See the NOTICE file
            # distributed with this work for additional information
            # regarding copyright ownership.  The ASF licenses this file
            # to you under the Apache License, Version 2.0 (the
            # "License"); you may not use this file except in compliance
            # with the License.  You may obtain a copy of the License at
            #
            #   http://www.apache.org/licenses/LICENSE-2.0
            #
            # Unless required by applicable law or agreed to in writing,
            # software distributed under the License is distributed on an
            # "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
            # KIND, either express or implied.  See the License for the
            # specific language governing permissions and limitations
            # under the License.
            save_dict = nd.load(params_path)
            arg_params = {}
            aux_params = {}
            for k, v in save_dict.items():
                tp, name = k.split(':', 1)
                if tp == 'arg':
                    arg_params[name] = v
                if tp == 'aux':
                    aux_params[name] = v
            mod = Module(symbol=symbol, context=Executor._prepare_ctx(ctx_config), logger=None)
            mod._arg_params = arg_params
            mod._aux_params = aux_params
            mod.params_initialized = True
            # TODO: There is a parameter named load_optimizer_states in Module.load
            return mod


@register(for_training=True)
class RCNNTrainer(Trainer):
    def __init__(self, symbol, train_iter, ctx, data_names, label_names, init_config, lr_config, opt_config,
                 resume_config, val_iter=None):
        super(RCNNTrainer, self).__init__(train_iter, init_config, lr_config, opt_config, val_iter=val_iter)
        pass

    @staticmethod
    def _prepare_module(symbol, ctx, resume_config):
        # TODO:
        pass
