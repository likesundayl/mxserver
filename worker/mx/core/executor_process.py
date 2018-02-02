# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from multiprocessing import Process

from worker.mx.core.executor import Executor
from worker.mx.db.mongo_connector import TaskProgressRecorder
from worker.mx.io.data_loader import load_data
from worker.mx.log.logger_generator import get_logger
from worker.mx.util.task_desc_parser import parse_task_desc, get_data_config
from worker.mx.util.time_getter import get_time
from worker.mx.util.exception_handler import exception_msg

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

        self._update_task_state('TASK_BEGIN_PREPARE_DATA')
        try:
            data_iters = load_data(for_training, exec_type, data_config)
            self._update_task_state('TASK_PREPARE_DATA_DONE')
        except StandardError, e:
            self._update_task_state('TASK_BEGIN_PREPARE_DATA_FAILED')
            excep_msg = exception_msg(e)
            _logger.error('Task_%s\'s DataIter instances creation failed! Because %s' % (self._process_id, excep_msg))
            return
        if for_training:
            executor_dict['train_iter'] = data_iters[0]
            if len(data_iters) == 1:
                executor_dict['val_iter'] = None
            else:
                executor_dict['val_iter'] = data_iters[1]
        else:
            executor_dict['data_batch_list'] = data_iters

        try:
            executor = Executor.create_executor(for_training=for_training, exec_type=exec_type, **executor_dict)
            self._update_task_state('TASK_EXECUTOR_CREATION_DONE')
            _logger.error('Task_%s\'s Executor instances creation done!' % self._process_id)
        except StandardError, e:
            self._update_task_state('TASK_EXECUTOR_CREATION_FAILED')
            _logger.error('Task_%s\'s Executor instances creation failed! Because %s' %
                          (self._process_id, exception_msg(e)))
            return

        try:
            self._update_task_state('TASK_BEGIN_RUNNING')
            _logger.info('Task_%s running is starting now' % self._process_id)
            executor.execute()
            self._update_task_state('TASK_DONE_SUCCESSFULLY')
            _logger.info('Task_%s running is done successfully' % self._process_id)
        except StandardError, e:
            self._update_task_state('TASK_TERMINATED_BY_INTERNAL_ERROR')
            excep_msg = exception_msg(e)
            _logger.error('Task_%s has been terminated by server internal error! Because %s' %
                          (self._process_id, excep_msg))

    def terminate(self):
        super(ExecutorProcess, self).terminate()
        self._update_task_state('TASK_TERMINATED_MANUALLY')
        _logger.info('Task_%s has been terminated manually' % self._process_id)

    def _update_task_state(self, task_state_desc):
        self._task_progress_list.append({'time': get_time(), 'task_state': task_state_desc})
        self._task_progress_recorder.update_one(self._process_id, self._task_progress_list)
