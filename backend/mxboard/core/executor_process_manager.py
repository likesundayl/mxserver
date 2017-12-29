# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import time

from multiprocessing import Process
from Queue import Empty

from backend.mxboard.log.logger_generator import get_logger


_logger = get_logger('executor_process_manager')


class ExecutorProcessManager(Process):
    def __init__(self, task_queue):
        super(ExecutorProcessManager, self).__init__()

        self._task_queue = task_queue

    def run(self):
        _logger.info('The executor_process_manager has been started')
        while True:
            try:
                executor_process = self._task_queue.get_nowait()
                _logger.info(
                    'executor_process_manager gets an ExecutorProcess instance from task queue, now start it')
                executor_process.run()
            except Empty:
                _logger.warn('The task queue is empty right now!')
            _logger.info('The executor_process_manager will sleep for 5 seconds')
            time.sleep(5)
