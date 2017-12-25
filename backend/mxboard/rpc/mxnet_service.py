# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.proto.mxboard_pb2_grpc import MXNetServiceServicer


class MXNetService(MXNetServiceServicer):
    def __init__(self):
        self._logger = get_logger('mxnet_service')

    def startTask(self, request, context):
        pass

    def stopTask(self, request, context):
        pass

