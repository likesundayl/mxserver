# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import time

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_time():
    """
    Get formatted time
    :return:
    """
    time.strftime(TIME_FORMAT, time.localtime())
