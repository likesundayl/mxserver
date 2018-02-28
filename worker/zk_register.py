# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 08/02/18 上午 09:11
"""
Register worker to ZooKeeper
"""
from socket import gethostname, getfqdn, gethostbyname

from kazoo.client import KazooClient

from util.conf_parser import mxserver_zk_config, mxserver_rpc_config

zk_worker_root_path = '/mxserver/worker'

host_name = gethostname()
ip_addr = gethostbyname(getfqdn(gethostname()))

worker_name = '%s_%s' % (host_name, ip_addr)


class ZkRegister(object):
    def __init__(self):
        if mxserver_zk_config['use-zk']:
            self._zk_cli = KazooClient(hosts=mxserver_zk_config['zk-hosts'], timeout=mxserver_zk_config['zk-timeout'])
            self._zk_cli.start(timeout=mxserver_zk_config['zk-timeout'])
            self._zk_cli.ensure_path(zk_worker_root_path)

    def register_worker_to_zk(self):
        if not mxserver_zk_config['use-zk']:
            return
        rpc_port = mxserver_rpc_config['port']
        rpc = '%s:%s' % (ip_addr, rpc_port)
        worker_path = zk_worker_root_path + '/%s' % worker_name
        if self._zk_cli.exists(worker_path):
            return
        self._zk_cli.create(path=worker_path, value=rpc, ephemeral=True)

    @staticmethod
    def use_zk():
        return mxserver_zk_config['use-zk']
