# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
from pymongo import MongoClient
from backend.mxboard.util.xml_parser import mxboard_mongo_config


class MongoConnector(object):
    def __init__(self):
        self._client = MongoClient(host=mxboard_mongo_config['host'], port=int(mxboard_mongo_config['port']))

    def close(self):
        self._client.close()
