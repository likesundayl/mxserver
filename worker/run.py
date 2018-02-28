# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 06/02/18 下午 04:38
import sys
import time
from multiprocessing import Queue

import grpc
from concurrent import futures

current_dir = sys.path[0]
index = current_dir.index('worker')
module_dir = current_dir[0:index]
sys.path.append(module_dir)

from util.logger_generator import get_logger
from worker.mxnet_extension.core.executor_process_manager import ExecutorProcessManager
from worker.proto import mxserver_pb2_grpc
from worker.rpc.mxnet_service import MXNetService
from util.conf_parser import mxserver_mxnet_config, mxserver_rpc_config, mxserver_task_queue_config
from util.exception_handler import exception_msg
from worker.zk_register import ZkRegister

# Add rcnn package to sys.path
sys.path.append(mxserver_mxnet_config['rcnn-path'])
print sys.path

if __name__ == '__main__':
    main_logger = get_logger('mxserver_worker_logger')
    try:
        if ZkRegister.use_zk():
            main_logger.info('The mxserver worker is trying to register to ZooKeeper')
        zk_register = ZkRegister()
        zk_register.register_worker_to_zk()
        if ZkRegister.use_zk():
            main_logger.info('The mxserver worker has registered to ZooKeeper')
    except BaseException as e:
        main_logger.error('The mxserver worker can not register to ZooKeeper! System exists! Error message: \n%s'
                          % exception_msg(e))
        sys.exit('Failed to register to ZooKeeper')
    task_queue = Queue(int(mxserver_task_queue_config['queue-max-size']))
    try:
        executor_process_manager = ExecutorProcessManager(task_queue=task_queue)
        executor_process_manager.start()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(mxserver_rpc_config['max-thread-num'])))
        mxserver_pb2_grpc.add_MXNetServiceServicer_to_server(MXNetService(task_queue), server)

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
    except BaseException as e:
        main_logger.error('The mxserver worker can not start! Error message: %s' % exception_msg(e))
