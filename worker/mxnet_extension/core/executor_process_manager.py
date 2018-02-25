# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import time
from Queue import Empty
from multiprocessing import Process

from util.logger_generator import get_logger

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
                task_id = executor_process.task_id()
                _logger.info(
                    'executor_process_manager gets an ExecutorProcess instance with task_id: %s from task queue, '
                    'now start it' % task_id)
                executor_process.start()
            except Empty:
                _logger.warn('The task queue is empty right now!')
            _logger.info('The executor_process_manager will sleep for 5 seconds')
            time.sleep(5)
