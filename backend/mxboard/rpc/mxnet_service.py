# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from backend.mxboard.log.logger_generator import get_logger


class MXNetService(object):
    def __init__(self):
        self._logger = get_logger('mxnet_service')

