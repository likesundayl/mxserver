# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 上午 11:48
"""
When a deep learning task request is received, the dispatcher will choose the best in-work worker, and
send a gRPC request to worker.
"""
from kazoo.client import KazooClient
from kazoo.exceptions import KazooException
from kazoo.handlers.threading import KazooTimeoutError

from util.conf_parser import mxserver_zk_config, mxserver_rpc_config

worker_zk_path = '/mxserver/worker'
assign_zk_path = '/mxserver/assign'


class Dispatcher(object):
    def __init__(self):
        self._name = 'dispatcher'

    @property
    def type(self):
        NotImplemented

    def choose_worker(self):
        NotImplemented

    def assign_task(self, task_id, worker_host):
        NotImplemented

    def find_worker_host_by_task_id(self, task_id):
        NotImplemented

    @staticmethod
    def create_dispatcher():
        if mxserver_zk_config['use-zk']:
            try:
                return ZkDispatcher()
            except KazooException:
                return DefaultDispatcher()
            except KazooTimeoutError:
                return DefaultDispatcher()
        else:
            return DefaultDispatcher()


class DefaultDispatcher(Dispatcher):
    def __init__(self):
        super(DefaultDispatcher, self).__init__()

    def type(self):
        return 'DefaultDispatcher'

    def choose_worker(self):
        return mxserver_rpc_config['host'] + ':' + str(mxserver_rpc_config['port'])

    def assign_task(self, task_id, worker_host):
        return

    def find_worker_host_by_task_id(self, task_id):
        return mxserver_rpc_config['host'] + ':' + str(mxserver_rpc_config['port'])


class ZkDispatcher(Dispatcher):
    def __init__(self):
        super(ZkDispatcher, self).__init__()
        self._zk_cli = KazooClient(hosts=mxserver_zk_config['zk-hosts'],
                                   timeout=mxserver_zk_config['zk-timeout'], logger=None)
        self._zk_cli.start()

    def type(self):
        return 'ZkDispatcher'

    def choose_worker(self):
        pass

    def assign_task(self, task_id, worker_host):
        pass

    def find_worker_host_by_task_id(self, task_id):
        pass
