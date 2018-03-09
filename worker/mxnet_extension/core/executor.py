# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017-present Terence Wu
# ------------------------------
"""
The extension of standard mxnet.module.Module
"""
from os import path as osp

from mxnet import nd
from mxnet import sym
from mxnet.module import Module

from numpy import squeeze, argsort

from worker.proto import mxserver_pb2

from util.conf_parser import mxserver_storage_config
from util.logger_generator import get_logger
from worker.db.mongo_connector import TestLogRecorder
from worker.mxnet_extension.core.callback import do_checkpoint, MongoTrainEvalMsgRecorder, MongoValEvalMsgRecorder
from worker.task_desc_parser import generate_ctx, generate_initializer, generate_lr_scheduler

params_root_path = mxserver_storage_config['params-root']

SUPPORTED_CLASSIFY_EVAL_METRICS = ['acc']
SUPPORTED_DETECTION_EVAL_METRICS = ['map']


class Executor(object):
    def __init__(self, task_id, classes):
        self._task_id = task_id
        self._classes = classes
        self._mod = None

    def execute(self):
        pass

    @staticmethod
    def _prepare_ctx(ctx_config):
        return generate_ctx(ctx_config)

    @staticmethod
    def load_check_point(sym_json_path, params_path, ctx_config_tuple, task_id):
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
        if not isinstance(sym_json_path, sym.Symbol):
            symbol = sym.load(sym_json_path)
        else:
            # If sym_json_path is already an instance of mxnet.sym.Symbol
            symbol = sym_json_path
        save_dict = nd.load(params_path)
        arg_params = {}
        aux_params = {}
        for k, v in save_dict.items():
            tp, name = k.split(':', 1)
            if tp == 'arg':
                arg_params[name] = v
            if tp == 'aux':
                aux_params[name] = v
        mod = Module(symbol=symbol, context=generate_ctx(ctx_config), logger=get_logger('mxnet_logger[tid=%s]' % task_id,
                                                                                        log_to_console=False,
                                                                                        log_to_file=True))
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
    def register(kclass):
        assert (isinstance(kclass, type))
        name = kclass.__name__.lower()
        try:
            name.index('trainer')
            if name not in Executor._registered_trainer:
                Executor._registered_trainer[name] = kclass
        except ValueError:
            if name not in Executor._registered_predictor:
                Executor._registered_predictor[name] = kclass
        return kclass


register = Executor.register


class Evaluator(Executor):
    def __init__(self, task_id, classes, sym_json_path, params_path, test_datas, eval_metrics=None,
                 ctx_config=({"device_name": "gpu", "device_id": "0"},), label=None):
        super(Evaluator, self).__init__(task_id=task_id, classes=classes)
        self._mod = Executor.load_check_point(task_id=task_id, sym_json_path=sym_json_path, params_path=params_path,
                                              ctx_config_tuple=ctx_config)
        self._eval_metrics = eval_metrics
        self._label = label
        self._test_datas = test_datas
        self._test_log_recorder = TestLogRecorder()

    def _eval(self):
        basic_msg = {
            'task_id': self._task_id,
            'test_raw_output': [],
            'test_eval_output': []
        }
        self._test_log_recorder.insert_one(basic_msg)

    def execute(self):
        self._eval()


@register
class ClassifyEvaluator(Evaluator):
    def __init__(self, task_id, classes, sym_json_path, params_path, test_datas, eval_metrics=None,
                 ctx_config=({"device_name": "gpu", "device_id": "0"},), label=None):
        super(ClassifyEvaluator, self).__init__(task_id=task_id, classes=classes, sym_json_path=sym_json_path,
                                                params_path=params_path, test_datas=test_datas,
                                                eval_metrics=eval_metrics,
                                                ctx_config=ctx_config, label=label)

    def _eval(self):
        super(ClassifyEvaluator, self)._eval()
        message = dict()
        message['raw'] = []
        message['eval'] = []
        # TODO: Rewrite

        self._test_log_recorder.update_one(self._task_id, message)

    @staticmethod
    def __eval(predicts, labels, eval_metric):
        if eval_metric in SUPPORTED_CLASSIFY_EVAL_METRICS:
            # TODO:
            return 0
        else:
            return None


@register
class ObjectDetectEvaluator(Evaluator):
    def __init__(self, task_id, classes, sym_json_path, params_path, test_datas, eval_metrics=None,
                 ctx_config=({"device_name": "gpu", "device_id": "0"},), label=None):
        super(ObjectDetectEvaluator, self).__init__(task_id=task_id, classes=classes, sym_json_path=sym_json_path,
                                                    params_path=params_path, test_datas=test_datas,
                                                    eval_metrics=eval_metrics,
                                                    ctx_config=ctx_config, label=label)

    def _eval(self):
        super(ObjectDetectEvaluator, self)._eval()
        # TODO: more work to do with object detection task


class Inferencer(Executor):
    def __init__(self, task_id, classes, sym_json_path, params_path, test_datas,
                 ctx_config=({"device_name": "gpu", "device_id": "0"},), top_k=1):
        super(Executor, self).__init__(task_id=task_id, classes=classes)
        self._mod = Executor.load_check_point(task_id=task_id, sym_json_path=sym_json_path, params_path=params_path,
                                              ctx_config_tuple=ctx_config)
        self._ctx_config = ctx_config
        self._test_datas = test_datas
        self._top_k = abs(top_k)

    def inference(self):
        raise NotImplementedError()


class ClassifyInferencer(Inferencer):
    def inference(self):
        cls_result = mxserver_pb2.ClsInferenceResult()
        for img, img_batch in self._test_datas.iteritems():
            self._mod.forward(img_batch, is_train=False)
            probs = self._mod.get_outputs()[0].asnumpy()
            probs = squeeze(probs)
            sorted_index = argsort(a=probs)
            for i in range(self._top_k):
                cls_result.result[img].top_k_probs.append(probs[i])
                cls_result.result[img].top_k_categorys.append(self._classes[str(sorted_index[i])])
        return cls_result


class ObjectDetectInference(Inferencer):
    def inference(self):
        pass


class Trainer(Executor):
    def __init__(self, task_id, classes, train_iter, init_config, lr_config, opt_config, save_prefix, save_period,
                 val_iter=None, eval_metrics=('acc',), begin_epoch=0, num_epoch=250, kvstore='local'):
        super(Trainer, self).__init__(task_id=task_id, classes=classes)
        self._initializer = Trainer._prepare_initializer(init_config)
        lr_scheduler = Trainer._prepare_lr_scheduler(lr_config)
        self._opt_type, self._mxnet_opt_params = Trainer._prepare_optimizer(opt_config)
        # lr_scheduler is a param of optimizer
        self._mxnet_opt_params['lr_scheduler'] = lr_scheduler
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
            MongoTrainEvalMsgRecorder(task_id=self._task_id)
        ]
        epoch_end_callbacks = [
            do_checkpoint(self._save_prefix, self._save_period)
        ]
        score_end_callbacks = [
            MongoValEvalMsgRecorder(task_id=self._task_id)
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
                      eval_end_callback=score_end_callbacks,
                      eval_batch_end_callback=None,
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


@register
class ClassifyTrainer(Trainer):
    def __init__(self, task_id, classes, symbol, train_iter, ctx_config, data_names, label_names, init_config,
                 lr_config, save_prefix, save_period, opt_config, resume_config, val_iter=None):
        super(ClassifyTrainer, self).__init__(task_id=task_id, classes=classes, train_iter=train_iter,
                                              init_config=init_config, lr_config=lr_config, opt_config=opt_config,
                                              save_prefix=save_prefix, save_period=save_period, val_iter=val_iter)
        self._mod = ClassifyTrainer._prepare_module(task_id=task_id, symbol=symbol, ctx_config=ctx_config,
                                                    data_names=data_names,
                                                    label_names=label_names, resume_config=resume_config)

    @staticmethod
    def _prepare_module(task_id, symbol, ctx_config, data_names, label_names, resume_config):
        if not resume_config['is_resume'] == '0':
            return Module(symbol=symbol, context=Executor._prepare_ctx(ctx_config), data_names=data_names,
                          label_names=label_names, logger=get_logger('mxnet_logger[tid=%s]' % task_id,
                                                                     log_to_console=False, log_to_file=True))
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
            mod = Module(symbol=symbol, context=Executor._prepare_ctx(ctx_config),
                         logger=get_logger('mxnet_logger[tid=%s]' % task_id, log_to_console=False, log_to_file=True))
            mod._arg_params = arg_params
            mod._aux_params = aux_params
            mod.params_initialized = True
            # TODO: There is a parameter named load_optimizer_states in Module.load
            return mod


@register
class RCNNTrainer(Trainer):
    def __init__(self, task_id, classes, symbol, train_iter, ctx, data_names, label_names, init_config, lr_config, opt_config,
                 resume_config, val_iter=None):
        super(RCNNTrainer, self).__init__(train_iter=train_iter, init_config=init_config, lr_config=lr_config,
                                          opt_config=opt_config, val_iter=val_iter,
                                          task_id=task_id)
        pass

    @staticmethod
    def _prepare_module(symbol, ctx, resume_config):
        # TODO:
        pass
