# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 06/02/18 下午 04:36
from os import mkdir
import os.path as osp
import logging
import logging.handlers as log_handlers
import time
import grpc
from flask import Flask, request, jsonify, make_response
import sys
current_dir = sys.path[0]
index = current_dir.index('flask_server')
module_dir = current_dir[0:index]
sys.path.append(module_dir)

from worker.mx.proto import mxboard_pb2, mxboard_pb2_grpc
from worker.mx.util.xml_parser import mxserver_log_config
from worker.mx.util.exception_handler import exception_msg
from worker.mx.gpu import gpu_monitor

# Check log dir
if not osp.exists('../log/flask'):
    mkdir('../log/flask')

current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = '../log/flask/mx-flask-server-' + current_date + '-log.txt'

file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                maxBytes=int(mxserver_log_config['log-max-bytes']),
                                                backupCount=int(mxserver_log_config['log-backup-count']))
console_handler = logging.StreamHandler()

formatter = logging.Formatter(mxserver_log_config['log-format'])
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

mxserver_flask_logger = logging.getLogger('mxserver_flask_server')

mxserver_flask_logger.addHandler(console_handler)
mxserver_flask_logger.addHandler(file_handler)

level = mxserver_log_config['log-level']
if level == 'INFO':
    mxserver_flask_logger.setLevel(logging.INFO)
elif level == 'DEBUG':
    mxserver_flask_logger.setLevel(logging.DEBUG)

# TODO:
channel = grpc.insecure_channel('127.0.0.1:50051')
stub = mxboard_pb2_grpc.MXNetServiceStub(channel)

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    task_json = request.json
    task_id = task_json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to start a train task with id: %s' % task_id)
    return jsonify(__task_state_2_json(__execute()))


@app.route('/predict', methods=['POST'])
def predict():
    task_json = request.json
    task_id = task_json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to start a test task with id: %s' % task_id)
    return jsonify(__execute())


@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.json['task_id']
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to stop a task with id: %s' % task_id)
    return jsonify(
        __task_state_2_json(stub.stopTask(mxboard_pb2.TaskId(id=task_id))))


@app.route('/gpu', methods=['GET'])
def query_gpu():
    mxserver_flask_logger.info('The mxserver_flask_server receives a request to query local GPU infos')
    try:
        result = gpu_monitor.query_gpu()
        response = make_response(result)
        response.headers['Content-Type'] = 'application/json'
        return response
    except StandardError as e:
        mxserver_flask_logger.error('The mxserver_flask_server fails to query local GPU infos! Error message: %s' %
                                    exception_msg(e))
        return jsonify([])


def __execute():
    task_json = request.json
    task_id = task_json['task_id']
    task_desc = task_json['task_desc']
    task_state = stub.startTask(mxboard_pb2.TaskParameter(id=mxboard_pb2.TaskId(task_id=task_id), task_desc=task_desc))
    return task_state


def __task_state_2_json(task_state):
    state_id = task_state.id
    state_code = task_state.state_code
    state_desc = task_state.state_desc
    return '{"task_id": "%s", "state_code": "%s", "state_desc": "%s"}' % (state_id, state_code, state_desc)


if __name__ == '__main__':
    mxserver_flask_logger.info('The mxboard_openapi_server has been started')
    app.run(host='0.0.0.0', port='5000')
