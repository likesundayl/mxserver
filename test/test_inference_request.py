# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:42
from requests import post
from test_resources import INFERENCE_TEST_URL, TEST_REQUEST_JSON
from util.logger_generator import get_logger
from util.exception_handler import exception_msg


if __name__ == '__main__':
    logger = get_logger('test_inference_request')
    logger.info('Begin to test API for deep learning inference')
    logger.info('Begin to send request to url: %s' % INFERENCE_TEST_URL)
    try:
        response = post(url=INFERENCE_TEST_URL, json=TEST_REQUEST_JSON)
        logger.info('Receive a response')
        logger.info('Response\'s status code: %s' % response.status_code)
        logger.info('Response\'s content: %s' % response.content)
    except BaseException as e:
        logger.error('Fail! Error message: %s\n' % exception_msg(e))
