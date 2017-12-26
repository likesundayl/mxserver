# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.proto import mxboard_pb2
from backend.mxboard.proto.mxboard_pb2_grpc import MXNetServiceServicer
from backend.mxboard.symbol.symbol_creater import create_symbol

SYMBOL_CREATE_STATE_CODES = [0, 1]
SYMBOL_CREATE_STATES = ['SUCCESSFUL', 'FAILED']


class MXNetService(MXNetServiceServicer):
    def __init__(self, task_queue):
        self._logger = get_logger('mxnet_service')
        self._queue = task_queue

    def createSymbol(self, request, context):
        symbol_name = request.symbol_name
        symbol_desc = request.symbol_desc
        self._logger.info('mxnet_service has received a new request to create a new symbol with name:%s' % symbol_name)
        if create_symbol(symbol_name, symbol_desc):
            return mxboard_pb2.SymbolCreateState(state_code=SYMBOL_CREATE_STATE_CODES[0],
                                                 state_desc=SYMBOL_CREATE_STATES[0])
        else:
            return mxboard_pb2.SymbolCreateState(state_code=SYMBOL_CREATE_STATE_CODES[1],
                                                 state_desc=SYMBOL_CREATE_STATES[1])

    def startTask(self, request, context):
        task_id = request.id
        self._logger.info('mxnet_service has received a new request to start a new task with id:%s' % task_id)
        # TODO:
        return mxboard_pb2.TaskState(state_code=0, state_desc='OK_TO_RUN')

    def stopTask(self, request, context):
        task_id = request.id
        self._logger.info('mxnet_service has received a new request to stop the task with id:%s' % task_id)
        # TODO:
        return mxboard_pb2.TaskState(state_code=0, state_desc='KILL_SUCCESSFULLY')


