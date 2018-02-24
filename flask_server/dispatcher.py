# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 上午 11:48
from kazoo.client import KazooClient

from util.xml_parser import mxsever_zk_config

worker_zk_path = '/mxserver/worker'
assign_zk_path = '/mxserver/assign'


class Dispatcher(object):
    def __init__(self):
        if not mxsever_zk_config['use-zk']:
            self._zk_cli = None
        else:
            self._zk_cli = KazooClient(hosts=mxsever_zk_config['zk-hosts'],
                                       timeout=mxsever_zk_config['zk-timeout'], logger=None)
            self._zk_cli.start()

    def choose_worker(self):
        if self._zk_cli is None:
            return '127.0.0.1:50051'

    def assign_task(self, task_id, worker_host):
        if self._zk_cli is None:
            return
        else:
            # TODO:
            return

    def find_worker_host_by_task_id(self, task_id):
        if self._zk_cli is None:
            return '127.0.0.1:50051'
