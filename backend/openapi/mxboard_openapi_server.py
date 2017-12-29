# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import grpc
from flask import Flask, request, jsonify
from backend.mxboard.proto import mxboard_pb2, mxboard_pb2_grpc

# TODO:
channel = grpc.insecure_channel('127.0.0.1:50051')
stub = mxboard_pb2_grpc.MXNetServiceStub(channel)

app = Flask(__name__)


@app.route('/train', methods=['POST'])
def train():
    return jsonify(__task_state_2_json(__execute()))


@app.route('/test', methods=['POST'])
def test():
    return jsonify(__execute())


@app.route('/stop', methods=['POST'])
def stop():
    return jsonify(
        __task_state_2_json(stub.stopTask(mxboard_pb2.TaskId(id=__get_stop_task_id()))))


def __execute():
    task_json = request.json
    task_id = task_json['task_id']
    task_desc = task_json['task_desc']
    task_state = stub.startTask(mxboard_pb2.TaskParameter(id=mxboard_pb2.TaskId(task_id=task_id), task_desc=task_desc))
    return task_state


def __get_stop_task_id():
    task_id = request.json['task_id']
    # TODO: some check work
    return task_id


def __task_state_2_json(task_state):
    state_id = task_state.id
    state_code = task_state.state_code
    state_desc = task_state.state_desc
    return '{"task_id": "%s", "state_code": "%s", "state_desc": "%s"}' % (state_id, state_code, state_desc)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
