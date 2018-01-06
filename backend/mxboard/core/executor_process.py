# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from multiprocessing import Process

from backend.config import EXCEPTION_MSG_LEVEL
from backend.mxboard.core.executor import Executor
from backend.mxboard.db.mongo_connector import TaskProgressRecorder
from backend.mxboard.io.data_loader import load_data_iter_rec
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.util.task_desc_parser import parse_task_desc, get_data_config
from backend.mxboard.util.time_getter import get_time

if EXCEPTION_MSG_LEVEL == 'DETAILED':
    import traceback

_logger = get_logger('executor_process')


class ExecutorProcess(Process):
    def __init__(self, process_id, task_desc):
        super(ExecutorProcess, self).__init__()
        self._task_progress_recorder = TaskProgressRecorder()
        self._process_id = process_id
        self._task_desc = task_desc
        self._task_progress_list = []

    def task_id(self):
        return self._process_id

    def run(self):
        self._task_progress_recorder.insert_one({
            'task_id': self._process_id,
            'task_progresses': []
        })

        for_training, exec_type, executor_dict = parse_task_desc(self._task_desc)
        executor_dict['task_id'] = self._process_id
        data_config = get_data_config(self._task_desc)

        # TODO: Prepare DataIters

        executor = Executor.create_executor(for_training=for_training, exec_type=exec_type, **executor_dict)

        try:
            self._update_task_state('TASK_BEGIN_RUNNING')
            _logger.info('Task_%s running is starting now' % self._process_id)
            executor.execute()
            self._update_task_state('TASK_DONE_SUCCESSFULLY')
            _logger.info('Task_%s running is done successfully' % self._process_id)
        except StandardError, e:
            self._update_task_state('TASK_TERMINATED_BY_INTERNAL_ERROR')
            if EXCEPTION_MSG_LEVEL == 'DETAILED':
                exception_msg = traceback.format_exc()
            elif EXCEPTION_MSG_LEVEL == 'BASIC':
                exception_msg = repr(e)
            else:
                exception_msg = str(e)
            _logger.error('Task_%s has been terminated by server internal error! Because %s' %
                          (self._process_id, exception_msg))

    def terminate(self):
        super(ExecutorProcess, self).terminate()
        self._update_task_state('TASK_TERMINATED_MANUALLY')
        _logger.info('Task_%s has been terminated manually' % self._process_id)

    def _update_task_state(self, task_state_desc):
        self._task_progress_list.append({'time': get_time(), 'task_state': task_state_desc})
        self._task_progress_recorder.update_one(self._process_id, self._task_progress_list)
