# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import xml.dom.minidom as xdm

xml_path = '../../../conf/mxboard.xml'


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

        return rpc_config

    def log_config(self):
        log_config = {}

        log_element = self._root.getElementsByTagName('log-conf')[0]
        log_config['log-format'] = log_element.getElementsByTagName('log-format')[0].firstChild.data
        log_config['log-max-bytes'] = log_element.getElementsByTagName('log-max-bytes')[0].firstChild.data
        log_config['log-backup-count'] = log_element.getElementsByTagName('log-backup-count')[0].firstChild.data
        log_config['log-level'] = log_element.getElementsByTagName('log-level')[0].firstChild.data

        return log_config


xml_parser = XMLParser()
mxboard_mongo_config = xml_parser.mongo_config()
mxboard_rpc_config = xml_parser.rpc_config()
mxboard_log_config = xml_parser.log_config()

