# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 下午 03:44
from socket import gethostname, getfqdn, gethostbyname

from kazoo.client import KazooClient

from util.conf_parser import mxserver_zk_config

zk_flask_root_path = '/mxserver/flask'

host_name = gethostname()
ip_addr = gethostbyname(getfqdn(gethostname()))

flask_server_name = '%s_%s' % (host_name, ip_addr)


class ZkRegister(object):
    def __init__(self):
        if mxserver_zk_config['use-zk']:
            self._zk_cli = KazooClient(hosts=mxserver_zk_config['zk-hosts'], timeout=mxserver_zk_config['zk-timeout'])
            self._zk_cli.start(timeout=mxserver_zk_config['zk-timeout'])
            self._zk_cli.ensure_path(flask_server_name)

    def register_flask_to_zk(self):
        if not mxserver_zk_config['use-zk']:
            return
        flask_port = mxserver_zk_config['port']
        flask = '%s:%s' % (ip_addr, flask_port)
        worker_path = zk_flask_root_path + '/%s' % flask_server_name
        if self._zk_cli.exists(worker_path):
            return
        self._zk_cli.create(path=worker_path, value=flask, ephemeral=True)

    @staticmethod
    def use_zk():
        return mxserver_zk_config['use-zk']
