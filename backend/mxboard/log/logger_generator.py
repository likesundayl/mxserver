# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import time
import logging
import logging.handlers as log_handlers

from backend.mxboard.util.xml_parser import mxboard_log_config


current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = '../../../log/mxboard-server-' + current_date + '-log.txt'


def get_logger(logger_name):
    handler = log_handlers.RotatingFileHandler(filename=log_file,
                                               maxBytes=long(mxboard_log_config['log-max-bytes']),
                                               backupCount=int(mxboard_log_config['log-backup-count']))
    formatter = logging.Formatter(mxboard_log_config['log-format'])
    handler.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    level = mxboard_log_config['log-level']
    if level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    return logger
