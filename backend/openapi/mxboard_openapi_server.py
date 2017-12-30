# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import logging
import logging.handlers as log_handlers
import time
import grpc
from flask import Flask, request, jsonify
import sys
current_dir = sys.path[0]
index = current_dir.index('backend')
module_dir = current_dir[0:index]
sys.path.append(module_dir)

from backend.mxboard.proto import mxboard_pb2, mxboard_pb2_grpc
from backend.mxboard.util.xml_parser import mxboard_log_config


current_date = time.strftime('%Y-%m-%d', time.localtime())
log_file = '../../log/mxboard-openapi-server-' + current_date + '-log.txt'

file_handler = log_handlers.RotatingFileHandler(filename=log_file,
                                                maxBytes=long(mxboard_log_config['log-max-bytes']),
                                                backupCount=int(mxboard_log_config['log-backup-count']))
console_handler = logging.StreamHandler()

formatter = logging.Formatter(mxboard_log_config['log-format'])
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

openapi_logger = logging.getLogger('mxboard_openapi_server')

openapi_logger.addHandler(console_handler)
openapi_logger.addHandler(file_handler)

level = mxboard_log_config['log-level']
if level == 'INFO':
    openapi_logger.setLevel(logging.INFO)
elif level == 'DEBUG':
    openapi_logger.setLevel(logging.DEBUG)

# TODO:
channel = grpc.insecure_channel('127.0.0.1:50051')
stub = mxboard_pb2_grpc.MXNetServiceStub(channel)

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    task_json = request.json
    task_id = task_json['task_id']
    openapi_logger.info('The mxboard_openapi_server receives a request to start a train task with id: %s' % task_id)
    return jsonify(__task_state_2_json(__execute()))


@app.route('/predict', methods=['POST'])
def predict():
    task_json = request.json
    task_id = task_json['task_id']
    openapi_logger.info('The mxboard_openapi_server receives a request to start a test task with id: %s' % task_id)
    return jsonify(__execute())


@app.route('/stop', methods=['POST'])
def stop():
    task_id = request.json['task_id']
    openapi_logger.info('The mxboard_openapi_server receives a request to stop a task with id: %s' % task_id)
    return jsonify(
        __task_state_2_json(stub.stopTask(mxboard_pb2.TaskId(id=task_id))))


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
    try:
        openapi_logger.info('The mxboard_openapi_server has been started')
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        openapi_logger.warn('The mxboard_openapi_server has been stopped manually!')
