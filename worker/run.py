# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 06/02/18 下午 04:38
import time
from multiprocessing import Queue
from kazoo.exceptions import KazooException

import grpc
from concurrent import futures

import sys
current_dir = sys.path[0]
index = current_dir.index('worker')
module_dir = current_dir[0:index]
sys.path.append(module_dir)

from worker.mx.log.logger_generator import get_logger
from worker.mx.core.executor_process_manager import ExecutorProcessManager
from worker.mx.proto import mxboard_pb2_grpc
from worker.mx.rpc.mxnet_service import MXNetService
from worker.mx.util.xml_parser import mxserver_rpc_config, mxserver_task_queue_config
from worker.mx.util.exception_handler import exception_msg
from worker.mx.zk_register import ZkRegister

if __name__ == '__main__':
    main_logger = get_logger('mxserver_worker_logger')
    try:
        zk_register = ZkRegister()
        zk_register.register_worker_to_zk()
    except KazooException as e:
        main_logger.error('The mxserver worker can not register to ZooKeeper! System exists! Error message: %s'
                          % exception_msg(e))
        sys.exit()
    task_queue = Queue(int(mxserver_task_queue_config['queue-max-size']))
    try:
        executor_process_manager = ExecutorProcessManager(task_queue=task_queue)
        executor_process_manager.start()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(mxserver_rpc_config['max-thread-num'])))
        mxboard_pb2_grpc.add_MXNetServiceServicer_to_server(MXNetService(task_queue), server)

        uri = mxserver_rpc_config['host'] + ':' + str(mxserver_rpc_config['port'])
        server.add_insecure_port(uri)

        server.start()
        main_logger.info('The mxserver worker has been started at: %s, waiting for request.' % uri)
        try:
            while True:
                time.sleep(int(mxserver_rpc_config['one-day-time-in-seconds']))
        except KeyboardInterrupt:
            main_logger.warn('The mxserver worker has been stopped manually!')
            server.stop(0)
    except StandardError as e:
        main_logger.error('The mxserver worker can not start! Error message: %s' % exception_msg(e))
