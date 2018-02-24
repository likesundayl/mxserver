# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging
import logging.handlers as log_handlers
import os.path as osp
import time

from util.xml_parser import mxserver_log_config

current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = osp.join(mxserver_log_config['log-file-root'], 'mx-server-' + current_date + '-log.txt')


def get_logger(logger_name):
    file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                    maxBytes=int(mxserver_log_config['log-max-bytes']),
                                                    backupCount=int(mxserver_log_config['log-backup-count']))
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(mxserver_log_config['log-format'])
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    level = mxserver_log_config['log-level']
    if level == 'INFO':
        logger.setLevel(logging.INFO)
    elif level == 'DEBUG':
        logger.setLevel(logging.DEBUG)

    return logger


a = 'home/womow/wuzhenan/ld'
index = a.index('/ld')
print a[0:index]
