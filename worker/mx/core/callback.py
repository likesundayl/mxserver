# -*- coding: utf-8 -*-

# @Time    : 2018/1/3 16:22
# @Author  : Terence Wu
# @License : Copyright (c) Terence Wu
from os import path as osp
from worker.mx.db.mongo_connector import TrainLogRecorder, ValLogRecorder
from worker.mx.util.xml_parser import mxserver_storage_config
from mxnet import nd, cpu

symbol_root_path = mxserver_storage_config['symbol-json-root']
params_root_path = mxserver_storage_config['params-root']


def do_checkpoint(prefix, period):
    # Copyed from MXNet and change a little

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
    period = int(max(1, period))

    def _callback(iter_no, sym, arg, aux):
        """The checkpoint function."""
        if (iter_no + 1) % period == 0:
            if sym is not None:
                sym.save(osp.join(symbol_root_path, '%s-symbol.json' % prefix))

            save_dict = {('arg:%s' % k): v.as_in_context(cpu()) for k, v in arg.items()}
            save_dict.update({('aux:%s' % k): v.as_in_context(cpu()) for k, v in aux.items()})
            param_name = osp.join(params_root_path, '%s-%04d.params' % (prefix, iter_no + 1))
            nd.save(param_name, save_dict)

    return _callback


class MongoEvalMsgRecorder(object):
    def __init__(self, task_id):
        self._task_id = task_id
        self._log_recorder = None
        self._eval_msgs = []

    def __call__(self, param):
        msg = {}
        eval_metric = param.eval_metric
        current_batch = param.nbatch
        msg['current_epoch'] = param.epoch
        msg['current_batch'] = current_batch
        metrics_result = eval_metric.get_name_value()
        for name, value in metrics_result:
            msg[name] = value
        self._eval_msgs.append(msg)
        self._log_recorder.update_one(self._task_id, self._eval_msgs)


class MongoTrainEvalMsgRecorder(MongoEvalMsgRecorder):
    def __init__(self, task_id):
        super(MongoTrainEvalMsgRecorder, self).__init__(task_id=task_id)
        self._log_recorder = TrainLogRecorder()


class MongoValEvalMsgRecorder(MongoEvalMsgRecorder):
    def __init__(self, task_id):
        super(MongoValEvalMsgRecorder, self).__init__(task_id=task_id)
        self._log_recorder = ValLogRecorder()

