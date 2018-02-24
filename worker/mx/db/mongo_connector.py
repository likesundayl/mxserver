# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from pymongo import MongoClient

from util.conf_parser import mxserver_mongo_config


class MongoConnector(object):
    def __init__(self):
        self._client = MongoClient(host=mxserver_mongo_config['host'], port=int(mxserver_mongo_config['port']))
        self._collection = None

    def insert_one(self, msg):
        self._collection.insert_one(msg)

    def update_one(self, task_id, msg):
        pass

    def close(self):
        self._client.close()


class TaskConfigRecorder(MongoConnector):
    def __init__(self):
        super(TaskConfigRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['basic-db']).get_collection('task-config')


class UserActionRecorder(MongoConnector):
    def __init__(self):
        super(UserActionRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['basic-db']).get_collection('user-action')


class TaskProgressRecorder(MongoConnector):
    def __init__(self):
        super(TaskProgressRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['task-db']).get_collection('task-progress')

    def update_one(self, task_id, msg):
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {'task_progresses': msg}}
        )


class TrainLogRecorder(MongoConnector):
    def __init__(self):
        super(TrainLogRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['train-db']).get_collection('train-log')

    def update_one(self, task_id, msg):
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {'train_eval_messages': msg}}
        )


class ValLogRecorder(MongoConnector):
    def __init__(self):
        super(ValLogRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['train-db']).get_collection('val-log')

    def update_one(self, task_id, msg):
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {'val_eval_messages': msg}}
        )


class TestLogRecorder(MongoConnector):
    def __init__(self):
        super(TestLogRecorder, self).__init__()
        self._collection = self._client.get_database(mxserver_mongo_config['test-db']).get_collection('test-log')

    def update_one(self, task_id, msg):
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {'test_raw_output': msg['raw']}}
        )
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {'test_eval_output': msg['eval']}}
        )
