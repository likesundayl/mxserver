# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging

##################################
# MXServer root path
##################################
MXSERVER_HOME = '/home/panyiming/wuzhenan/open_source_projects/mxserver'

#################################################
# Available levels: 'SIMPLE', 'BASIC', 'DETAILED'
#################################################
EXCEPTION_MSG_LEVEL = 'DETAILED'

##################################
# RCNN Package path in MXNet
##################################
RCNN_PACKAGE_PATH = ''

##################################
# Mongo Config
##################################
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017
MONGO_BASIC_DB_NAME = 'basic'
MONGO_TASK_DB_NAME = 'task'
MONGO_TRAIN_DB_NAME = 'train'
MONGO_TEST_DB_NAME = 'test'

##################################
# RPC Config
##################################
RPC_HOST = '127.0.0.1'
RPC_PORT = 50051
RPC_MAX_THREAD_NUM = 4
RPC_ONE_DAY_TIME_IN_SECONDS = 86400

##################################
# Flask Config
##################################
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

##################################
# ZooKeeper Config
##################################
USE_ZK = False
ZK_TIMEOUT = 5
ZK_HOSTS = ['127.0.0.1:2181']

##################################
# Logger Config
##################################
LOG_TO_FILE = False
LOG_FORMAT = '%(asctime)s - %(filename)s-%(lineno)s[%(levelname)s]: %(message)s'
LOG_MAX_BYTES = 10485760
LOG_BACKUP_COUNT = 5
LOG_LEVEL = logging.INFO

##################################
# Task Queue Config
##################################
TASK_QUEUE_MAX_SIZE = 10
TASK_QUEUE_WAIT_TIMEOUT = 10

##################################
# Data download Config
##################################
DATA_DOWNLOAD_MAX_RETRY_NUM = 5
