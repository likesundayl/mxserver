# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:36
from requests import post
from test_resources import TRAIN_TEST_URL, TRAIN_REQUEST_JSON
from util.logger_generator import get_logger
from util.exception_handler import exception_msg


if __name__ == '__main__':
    logger = get_logger('test_train_request')
    logger.info('Begin to test API for deep learning training')
    logger.info('Begin to send request to url: %s' % TRAIN_TEST_URL)
    try:
        response = post(url=TRAIN_TEST_URL, json=TRAIN_REQUEST_JSON)
        logger.info('Receive a response')
        logger.info('Response\'s status code: %s' % response.status_code)
        logger.info('Response\'s content: %s' % response.content)
    except StandardError as e:
        logger.error('Fail! Error message: %s\n' % exception_msg(e))
