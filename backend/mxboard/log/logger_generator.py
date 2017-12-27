# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging
import logging.handlers as log_handlers
import time

from backend.mxboard.util.xml_parser import mxboard_log_config

current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = '../../../log/mxboard-server-' + current_date + '-log.txt'


def get_logger(logger_name):
    file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                    maxBytes=long(mxboard_log_config['log-max-bytes']),
                                                    backupCount=int(mxboard_log_config['log-backup-count']))
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(mxboard_log_config['log-format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    level = mxboard_log_config['log-level']
    if level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    return logger
