# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging
import logging.handlers as log_handlers
import os.path as osp
import time

from util.conf_parser import mxserver_log_config

current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = osp.join(mxserver_log_config['log-file-root'], 'mx-server-' + current_date + '-log.txt')


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(mxserver_log_config['log-level'])

    formatter = logging.Formatter(mxserver_log_config['log-format'])

    if mxserver_log_config['log-to-file']:
        file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                        maxBytes=int(mxserver_log_config['log-max-bytes']),
                                                        backupCount=int(mxserver_log_config['log-backup-count']))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
