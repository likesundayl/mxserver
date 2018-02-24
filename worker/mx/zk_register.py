# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 08/02/18 上午 09:11
from socket import gethostname, getfqdn, gethostbyname

from kazoo.client import KazooClient

from util.xml_parser import mxsever_zk_config, mxserver_rpc_config

zk_worker_root_path = '/mxserver/worker'
worker_name = '%s_%s' % (gethostname(), gethostbyname(getfqdn(gethostname())))


class ZkRegister(object):
    def __init__(self):
        if mxsever_zk_config['use-zk']:
            self._zk_cli = KazooClient(hosts=mxsever_zk_config['zk-hosts'], timeout=mxsever_zk_config['zk-timeout'])
            self._zk_cli.start(timeout=mxsever_zk_config['zk-timeout'])
            self._zk_cli.ensure_path(zk_worker_root_path)

    def register_worker_to_zk(self):
        if not mxsever_zk_config['use-zk']:
            return
        rpc_host = mxserver_rpc_config['host']
        rpc_port = mxserver_rpc_config['port']
        rpc = '%s:%s' % (rpc_host, rpc_port)
        worker_path = zk_worker_root_path + '/%s' % worker_name
        if self._zk_cli.exists(worker_path):
            return
        self._zk_cli.create(path=worker_path, value=rpc, ephemeral=True)
