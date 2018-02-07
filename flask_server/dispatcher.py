# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 上午 11:48
from worker.mx.util.xml_parser import mxsever_zk_config
from kazoo.client import KazooClient

worker_zk_path = '/mxserver/worker'
assign_zk_path = '/mxserver/assign'


class Dispatcher(object):
    def __init__(self):
        if len(mxsever_zk_config['zk-hosts']) == 0:
            self._zk_cli = None
        else:
            self._zk_cli = KazooClient(hosts=mxsever_zk_config['zk-hosts'],
                                       timeout=mxsever_zk_config['zk-timeout'])
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
