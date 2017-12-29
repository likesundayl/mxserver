# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import xml.dom.minidom as xdm
from backend.config import CONFIG_XML_PATH

xml_path = CONFIG_XML_PATH


class XMLParser(object):
    def __init__(self):
        self._root = xdm.parse(xml_path).documentElement

    def mongo_config(self):
        mongo_config = {}
        mongo_element = self._root.getElementsByTagName('mongo-conf')[0]

        mongo_config['host'] = mongo_element.getElementsByTagName('host')[0].firstChild.data
        mongo_config['port'] = mongo_element.getElementsByTagName('port')[0].firstChild.data
        mongo_config['task-db'] = mongo_element.getElementsByTagName('task-db')[0].firstChild.data
        mongo_config['train-db'] = mongo_element.getElementsByTagName('train-db')[0].firstChild.data
        mongo_config['test-db'] = mongo_element.getElementsByTagName('test-db')[0].firstChild.data

        return mongo_config

    def rpc_config(self):
        rpc_config = {}
        rpc_element = self._root.getElementsByTagName('rpc-conf')[0]

        rpc_config['host'] = rpc_element.getElementsByTagName('host')[0].firstChild.data
        rpc_config['port'] = rpc_element.getElementsByTagName('port')[0].firstChild.data
        rpc_config['max-thread-num'] = rpc_element.getElementsByTagName('max-thread-num')[0].firstChild.data
        rpc_config['one-day-time-in-seconds'] = rpc_element.getElementsByTagName('one-day-time-in-seconds')[0] \
            .firstChild.data

        return rpc_config

    def log_config(self):
        log_config = {}

        log_element = self._root.getElementsByTagName('log-conf')[0]
        log_config['log-format'] = log_element.getElementsByTagName('log-format')[0].firstChild.data
        log_config['log-max-bytes'] = log_element.getElementsByTagName('log-max-bytes')[0].firstChild.data
        log_config['log-backup-count'] = log_element.getElementsByTagName('log-backup-count')[0].firstChild.data
        log_config['log-level'] = log_element.getElementsByTagName('log-level')[0].firstChild.data

        return log_config

    def storage_config(self):
        storage_config = {}

        storage_element = self._root.getElementsByTagName('storage-conf')[0]
        storage_config['symbol-json-root'] = storage_element.getElementsByTagName('symbol-json-root')[0].firstChild.data
        storage_config['params-root'] = storage_element.getElementsByTagName('params-root')[0].firstChild.data

        return storage_config

    def task_queue_config(self):
        task_queue_config = {}

        task_element = self._root.getElementsByTagName('task-queue-conf')[0]
        task_queue_config['queue-max-size'] = task_element.getElementsByTagName('queue-max-size')[0].firstChild.data
        task_queue_config['wait-time-out'] = task_element.getElementsByTagName('wait-time-out')[0].firstChild.data

        return task_queue_config

    def data_download_config(self):
        data_download_config = {}

        data_element = self._root.getElementsByTagName('data-download-conf')[0]
        data_download_config['max-retry-num'] = data_element.getElementsByTagName('max-retry-num')[0].firstChild.data

        return data_download_config


xml_parser = XMLParser()
mxboard_mongo_config = xml_parser.mongo_config()
mxboard_rpc_config = xml_parser.rpc_config()
mxboard_log_config = xml_parser.log_config()
mxboard_storage_config = xml_parser.storage_config()
mxboard_task_queue_config = xml_parser.task_queue_config()
mxboard_data_download_config = xml_parser.data_download_config()
