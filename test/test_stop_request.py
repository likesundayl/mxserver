# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:37
from requests import post
from test_resources import STOP_TEST_URL, STOP_REQUEST_JSON
from util.logger_generator import get_logger
from util.exception_handler import exception_msg


if __name__ == '__main__':
    logger = get_logger('test_stop_request')
    logger.info('Begin to test API for deep learning training')
    logger.info('Begin to send request to url: %s' % STOP_TEST_URL)
    try:
        response = post(url=STOP_TEST_URL, json=STOP_REQUEST_JSON)
        logger.info('Receive a response')
        logger.info('Response\'s status code: %s' % response.status_code)
        logger.info('Response\'s content: %s' % response.content)
    except StandardError as e:
        logger.error('Fail! Error message: %s\n' % exception_msg(e))
