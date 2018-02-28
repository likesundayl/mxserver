# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 28/02/18 上午 10:22
from kafka import KafkaProducer
from util.conf_parser import mxserver_kafka_config


class MsgPusher(object):
    def __init__(self, task_id):
        self._producer = KafkaProducer(bootstrap_servers=mxserver_kafka_config['hosts'])
        self._task_id = task_id
        self._msg_topic = ''

    def push_msg(self, msg):
        self._producer.send(topic=self._msg_topic, value=msg)


class TrainLogMsgPusher(MsgPusher):
    def __init__(self, task_id):
        super(TrainLogMsgPusher, self).__init__(task_id=task_id)
        self._msg_topic = 'train_log_%s' % self._task_id


class ValLogMsgPusher(MsgPusher):
    def __init__(self, task_id):
        super(ValLogMsgPusher, self).__init__(task_id=task_id)
        self._msg_topic = 'val_log_%s' % self._task_id


class TestLogPusher(MsgPusher):
    def __init__(self, task_id):
        super(TestLogPusher, self).__init__(task_id=task_id)
        self._msg_topic = 'test_log_%s' % self._task_id

