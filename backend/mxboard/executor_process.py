# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from multiprocessing import Process
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.executor import Executor
from backend.mxboard.util.task_desc_parser import parse_task_desc, get_data_and_label_names
from backend.mxboard.io.data_loader import load_data_iter_rec

_logger = get_logger('executor_process')


class ExecutorProcess(Process):
    def __init__(self, process_id, task_desc):
        super(ExecutorProcess, self).__init__()
        self._process_id = process_id
        self._task_desc = task_desc

    def run(self):
        symbol, ctx_list, data_dict, initializer, lr_scheduler, optimizer = parse_task_desc(self._task_desc)
        data_names, label_names = get_data_and_label_names(data_dict)
        # TODO:
        data_iters = load_data_iter_rec(data_dict)
        return Executor(symbol=symbol, data_iters=data_iters, ctx_list=ctx_list, initializer=initializer,
                        lr_scheduler=lr_scheduler, optimizer=optimizer, data_names=data_names, label_names=label_names)
        # TODO: lots of work to do
        self._executor.execute()

    def terminate(self):
        super(ExecutorProcess, self).terminate()


