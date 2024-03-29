# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 06/02/18 下午 04:36
import sys
from flask import Flask, request, jsonify, make_response

import grpc

current_dir = sys.path[0]
index = current_dir.index('flask_server')
module_dir = current_dir[0:index]
sys.path.append(module_dir)

from worker.proto import mxserver_pb2, mxserver_pb2_grpc
from util.conf_parser import mxserver_flask_config
from util.exception_handler import exception_msg
from util.logger_generator import get_logger
from worker.gpu import gpu_monitor
from dispatcher import Dispatcher
from flask_server.zk_register import ZkRegister

mxserver_flask_logger = get_logger('mxserver_flask_server')

dispatcher = Dispatcher.create_dispatcher()
mxserver_flask_logger.info('The mxserver flask server has created a dispatcher with type: %s' % dispatcher.type())

app = Flask('MXServer-Flask-Server')


@app.route('/train', methods=['POST'])
def train():
    task_json = request.json
    task_id = task_json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to start a train task with id: %s' % task_id)
    return jsonify(__task_state_2_json(__execute()))


@app.route('/eval', methods=['POST'])
def evaluate():
    task_json = request.json
    task_id = task_json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to start a evaluation task with id: %s'
                               % task_id)
    return jsonify(__execute())


@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to stop a task with id: %s' % task_id)
    # TODO:
    worker_host = dispatcher.find_worker_host_by_task_id(task_id)
    mxserver_flask_logger.info('The mxserver_flask_server has found task: %s at worker: %s' % (task_id, worker_host))
    channel = grpc.insecure_channel(worker_host)
    stub = mxserver_pb2_grpc.MXNetServiceStub(channel)

    return jsonify(
        __task_state_2_json(stub.stopTask(mxserver_pb2.TaskId(id=task_id))))


@app.route('/deploy', methods=['POST'])
def deploy():
    pass


@app.route('/classify', methods=['POST'])
def classify():
    pass


@app.route('/detect', methods=['POST'])
def object_detect():
    pass


@app.route('/gpu', methods=['GET'])
def query_gpu():
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to query local GPU infos')
    try:
        result = gpu_monitor.query_gpu()
        response = make_response(result)
        response.headers['Content-Type'] = 'application/json'
        return response
    except BaseException as e:
        mxserver_flask_logger.error('The mxserver_flask_server fails to query local GPU infos! Error message: %s' %
                                    exception_msg(e))
        return jsonify([])


def __execute():
    task_json = request.json
    task_id = task_json['task_id']
    task_desc = task_json['task_desc']
    # Choose available worker
    worker_host = dispatcher.choose_worker()

    channel = grpc.insecure_channel(worker_host)
    stub = mxserver_pb2_grpc.MXNetServiceStub(channel)

    task_state = stub.startTask(mxserver_pb2.TaskParameter(id=mxserver_pb2.TaskId(task_id=task_id), task_desc=task_desc))
    if task_state.state_code == 0:
        dispatcher.assign_task(task_id, worker_host)
    return task_state


def __task_state_2_json(task_state):
    state_id = task_state.id
    state_code = task_state.state_code
    state_desc = task_state.state_desc
    return '{"task_id": "%s", "state_code": "%s", "state_desc": "%s"}' % (state_id, state_code, state_desc)


if __name__ == '__main__':
    try:
        if ZkRegister.use_zk():
            mxserver_flask_logger.info('The mxserver flask server is trying to register to ZooKeeper')
        zk_register = ZkRegister()
        zk_register.register_flask_to_zk()
        if ZkRegister.use_zk():
            mxserver_flask_logger.info('The mxserver flask server has registered to ZooKeeper')
    except BaseException as e:
        mxserver_flask_logger.error('The mxserver flask server can not register to ZooKeeper! System exists! '
                                    'Error message: \n%s' % exception_msg(e))
        sys.exit('Failed to register to ZooKeeper')

    mxserver_flask_logger.info('The mxserver flask server has been started')
    app.run(host=mxserver_flask_config['host'], port=mxserver_flask_config['port'])
