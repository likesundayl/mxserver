# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from pymongo import MongoClient

from backend.mxboard.util.xml_parser import mxboard_mongo_config


class MongoConnector(object):
    def __init__(self):
        self._client = MongoClient(host=mxboard_mongo_config['host'], port=int(mxboard_mongo_config['port']))
        self._collection = None

    def insert_one(self, msg):
        self._collection.insert_one(msg)

    def update_one(self, task_id, msg):
        pass

    def close(self):
        self._client.close()


class TaskProgressRecorder(MongoConnector):
    def __init__(self):
        super(TaskProgressRecorder, self).__init__()
        self._collection = self._client.get_database('task-db').get_collection('task-progress')

    def update_one(self, task_id, msg):
        self._collection.update_one(
            {'task_id': task_id},
            {'$set': {}}
        )
