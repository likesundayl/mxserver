# -*- coding: utf-8 -*-

# @Time    : 2018/1/3 16:22
# @Author  : Terence Wu
# @License : Copyright (c) Terence Wu
from backend.mxboard.db.mongo_connector import TrainLogRecorder


class MongoEvalMsgRecorder(object):
    def __init__(self, task_id):
        self._task_id = task_id
        self._train_log_recorder = TrainLogRecorder()
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
        self._train_log_recorder.update_one(self._task_id, self._eval_msgs)


