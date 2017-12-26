# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.symbol.symbol_creater import create_symbol
from backend.mxboard.proto import mxboard_pb2
from backend.mxboard.proto.mxboard_pb2_grpc import MXNetServiceServicer


SYMBOL_CREATE_STATE_CODES = [0, 1]
SYMBOL_CREATE_STATES = ['SUCCESSFUL', 'FAILED']


class MXNetService(MXNetServiceServicer):
    def __init__(self, task_queue):
        self._logger = get_logger('mxnet_service')
        self._queue = task_queue

    def createSymbol(self, request, context):
        symbol_name = request.symbol_name
        symbol_desc = request.symbol_desc
        if create_symbol(symbol_name, symbol_desc):
            return mxboard_pb2.SymbolCreateState(state_code=SYMBOL_CREATE_STATE_CODES[0],
                                                 state_desc=SYMBOL_CREATE_STATES[0])
        else:
            return mxboard_pb2.SymbolCreateState(state_code=SYMBOL_CREATE_STATE_CODES[1],
                                                 state_desc=SYMBOL_CREATE_STATES[1])

    def startTask(self, request, context):
        pass

    def stopTask(self, request, context):
        pass

