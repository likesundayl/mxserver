# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import time
from multiprocessing import Queue

import grpc
from concurrent import futures

from backend.mxboard.executor_process_manager import ExecutorProcessManager
from backend.mxboard.log.logger_generator import get_logger
from backend.mxboard.proto import mxboard_pb2_grpc
from backend.mxboard.rpc.mxnet_service import MXNetService
from backend.mxboard.util.xml_parser import mxboard_rpc_config, mxboard_task_queue_config

if __name__ == '__main__':
    main_logger = get_logger('mxnet_server')

    task_queue = Queue(int(mxboard_task_queue_config['queue-max-size']))
    try:
        executor_process_manager = ExecutorProcessManager(task_queue=task_queue)
        executor_process_manager.start()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(mxboard_rpc_config['max-thread-num'])))
        mxboard_pb2_grpc.add_MXNetServiceServicer_to_server(MXNetService(task_queue), server)

        uri = mxboard_rpc_config['host'] + ':' + mxboard_rpc_config['port']
        server.add_insecure_port(uri)

        server.start()
        main_logger.info('MXNet server has been started at: %s, waiting for request.' % uri)
        try:
            while True:
                time.sleep(int(mxboard_rpc_config['one-day-time-in-seconds']))
        except KeyboardInterrupt:
            main_logger.warn('MXNet server has been stopped!')
            server.stop(0)
    except StandardError:
        main_logger.error('The mxnet_server can not be started!')
