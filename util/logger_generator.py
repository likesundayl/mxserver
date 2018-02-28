# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging
import logging.handlers as log_handlers
import os.path as osp
import time
from os import mkdir

from util.conf_parser import mxserver_log_config

if mxserver_log_config['log-to-file']:
    current_date = time.strftime('%Y-%m-%d', time.localtime())
    new_log_file_root = osp.join(mxserver_log_config['log-file-root'], current_date)
    if not osp.exists(new_log_file_root):
        mkdir(new_log_file_root)


def get_logger(logger_name, log_to_console=True, log_to_file=False):
    logger = logging.getLogger(logger_name)
    logger.setLevel(mxserver_log_config['log-level'])

    formatter = logging.Formatter(mxserver_log_config['log-format'])

    if mxserver_log_config['log-to-file'] or log_to_file:
        log_file = osp.join(new_log_file_root, logger_name + '.txt')
        file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                        maxBytes=int(mxserver_log_config['log-max-bytes']),
                                                        backupCount=int(mxserver_log_config['log-backup-count']))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger
