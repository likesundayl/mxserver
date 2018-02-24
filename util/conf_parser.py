# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from os.path import exists
from os import mkdir
import config as cfg

mxserver_mxnet_config = {
    'rcnn-path': cfg.RCNN_PACKAGE_PATH
}
mxserver_mongo_config = {
    'host': cfg.MONGO_HOST,
    'port': cfg.MONGO_PORT,
    'basic-db': cfg.MONGO_BASIC_DB_NAME,
    'task-db': cfg.MONGO_TASK_DB_NAME,
    'train-db': cfg.MONGO_TRAIN_DB_NAME,
    'test-db': cfg.MONGO_TEST_DB_NAME
}
mxserver_rpc_config = {
    'host': cfg.RPC_HOST,
    'port': cfg.RPC_PORT,
    'max-thread-num': cfg.RPC_MAX_THREAD_NUM,
    'one-day-time-in-seconds': cfg.RPC_ONE_DAY_TIME_IN_SECONDS
}
mxserver_flask_config = {
    'host': cfg.FLASK_HOST,
    'port': str(cfg.FLASK_PORT)
}
mxsever_zk_config = {
    'use-zk': cfg.USE_ZK,
    'zk-timeout': cfg.ZK_TIMEOUT,
    'zk-hosts': cfg.ZK_HOSTS
}
# Check work
if not exists(cfg.LOG_FILE_ROOT):
    mkdir(cfg.LOG_FILE_ROOT)
mxserver_log_config = {
    'log-file-root': cfg.LOG_FILE_ROOT,
    'log-format': cfg.LOG_FORMAT,
    'log-max-bytes': cfg.LOG_MAX_BYTES,
    'log-backup-count': cfg.LOG_BACKUP_COUNT,
    'log-level': cfg.LOG_LEVEL
}
# Check work
if not exists(cfg.REC_ROOT):
    mkdir(cfg.REC_ROOT)
if not exists(cfg.SYMBOL_JSON_ROOT):
    mkdir(cfg.SYMBOL_JSON_ROOT)
if not exists(cfg.PARAMS_ROOT):
    mkdir(cfg.PARAMS_ROOT)
mxserver_storage_config = {
    'rec-root': cfg.REC_ROOT,
    'symbol-json-root': cfg.SYMBOL_JSON_ROOT,
    'params-root': cfg.PARAMS_ROOT
}
mxserver_task_queue_config = {
    'queue-max-size': cfg.TASK_QUEUE_MAX_SIZE,
    'wait-time-out': cfg.TASK_QUEUE_WAIT_TIMEOUT
}
mxserver_data_download_config = {
    'max-retry-num': cfg.DATA_DOWNLOAD_MAX_RETRY_NUM
}
