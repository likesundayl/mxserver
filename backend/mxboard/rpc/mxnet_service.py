# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from Queue import Full

from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.db.mongo_connector import TaskConfigRecorder, UserActionRecorder
from backend.mxboard.core.executor_process import ExecutorProcess
from backend.mxboard.proto import mxboard_pb2
from backend.mxboard.proto.mxboard_pb2_grpc import MXNetServiceServicer
from backend.mxboard.symbol.symbol_creater import create_symbol
from backend.mxboard.util.time_getter import get_time
from backend.config import EXCEPTION_MSG_LEVEL

if EXCEPTION_MSG_LEVEL == 'DETAILED':
    import traceback

MAX_TRY_TIMES = 5
# symbol state codes and states descs
SYMBOL_CREATE_STATE_CODES = [0, 1]
SYMBOL_CREATE_STATES = ['SUCCESSFUL', 'FAILED']
# task state codes and states descs
TASK_STATE_CODES = [0, 1]
TASK_STATES = ['OK_TO_RUN', 'FULL_QUEUE', 'TASK_NOT_EXIST', 'TASK_TERMINATED_SUCCESSFULLY', 'TASK_TERMINATED_FAILED']


class MXNetService(MXNetServiceServicer):
    def __init__(self, task_queue):
        self._logger = get_logger('mxnet_service')
        self._queue = task_queue
        self._task_config_recorder = TaskConfigRecorder()
        self._user_action_recorder = UserActionRecorder()
        self._task_dict = {}

    def createSymbol(self, request, context):
        symbol_id = request.symbol_id
        symbol_name = request.symbol_name
        symbol_desc = request.symbol_desc

        self._logger.info('The mxnet_service has received a new request to create a new symbol with name:%s' %
                          symbol_name)
        self._record_user_action(symbol_id, 'create_symbol')

        if create_symbol(symbol_name, symbol_desc):
            return mxboard_pb2.SymbolCreateState(symbol_id=symbol_id,
                                                 state_code=SYMBOL_CREATE_STATE_CODES[0],
                                                 state_desc=SYMBOL_CREATE_STATES[0])
        else:
            return mxboard_pb2.SymbolCreateState(symbol_id=symbol_id,
                                                 state_code=SYMBOL_CREATE_STATE_CODES[1],
                                                 state_desc=SYMBOL_CREATE_STATES[1])

    def startTask(self, request, context):
        task_id = request.id

        self._logger.info('The mxnet_service has received a new request to start a new task with id:%s' % task_id)
        self._record_user_action(task_id, 'start_task')

        task_desc = request.task_desc

        # Put basic task config to MongoDB
        self._task_config_recorder.insert_one(task_desc)

        executor_process = ExecutorProcess(process_id=task_id, task_desc=task_desc)
        try_times = 1
        while try_times <= MAX_TRY_TIMES:
            try:
                self._queue.put_nowait(executor_process)
                self._task_dict[task_id] = executor_process
                self._logger.info('The mxnet_service has put an ExecutorProcess instance to task queue')

                return mxboard_pb2.TaskState(task_id=task_id, state_code=TASK_STATE_CODES[0],
                                             state_desc=TASK_STATES[0])
            except Full:
                self._logger.warn('The mxnet_service can not put an ExecutorProcess instance to task queue because task'
                                  ' queue is full right now! Try again, totally try %d times!' % try_times)
            try_times += 1

        self._logger.error('The mxnet_service failed to put an ExecutorProcess instance to task queue because task is '
                           'full for too long!')
        return mxboard_pb2.TaskState(task_id=task_id, state_code=TASK_STATE_CODES[1],
                                     state_desc=TASK_STATES[1])

    def stopTask(self, request, context):
        task_id = request.id

        self._logger.info('mxnet_service has received a new request to stop the task with id:%s' % task_id)
        self._record_user_action(task_id, 'stop_task')

        executor_process = self._task_dict.get(task_id)
        if executor_process is None:
            self._logger.warn('mxnet_service can not find a task with id: %s' % task_id)
            return mxboard_pb2.TaskState(task_id=task_id, state_code=TASK_STATE_CODES[1],
                                         state_desc=TASK_STATES[2])
        else:
            try:
                executor_process.terminate()
                self._logger.warn('mxnet_service has terminated the task with id: %s' % task_id)
                # After terminate, the key-value should be deleted
                del self._task_dict[task_id]
                return mxboard_pb2.TaskState(task_id=task_id, state_code=TASK_STATE_CODES[0],
                                             state_desc=TASK_STATES[3])
            except StandardError, e:
                if EXCEPTION_MSG_LEVEL == 'DETAILED':
                    exception_msg = traceback.format_exc()
                elif EXCEPTION_MSG_LEVEL == 'BASIC':
                    exception_msg = repr(e)
                else:
                    exception_msg = str(e)
                self._logger.warn('mxnet_service can not terminate the task with id: %s! Because %s' %
                                  (task_id, exception_msg))
                return mxboard_pb2.TaskState(task_id=task_id, state_code=TASK_STATE_CODES[1],
                                             state_desc=TASK_STATES[4])

    def _record_user_action(self, task_id, action_name):
        action_occur_time = get_time()
        action_desc = {
            'action_obj_id': task_id,
            'action_time': action_occur_time,
            'action_name': action_name
        }
        self._user_action_recorder.insert_one(action_desc)
