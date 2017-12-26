# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from multiprocessing import Process
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.executor import Executor


class ExecutorProcess(Process):
    def __init__(self, process_id, task_desc):
        super(ExecutorProcess, self).__init__()
        self._process_id = process_id
        self._logger = get_logger('executor_process_%s' % process_id)
        self._executor = self._init_executor(task_desc)

    def _init_executor(self, task_desc):
        # TODO:
        return Executor()

    def run(self):
        # TODO: lots of work to do
        self._executor.execute()

    def terminate(self):
        super(ExecutorProcess, self).terminate()
