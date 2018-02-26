# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:37
from requests import get
from test_resources import QUERY_GPU_TEST_URL
from util.logger_generator import get_logger
from util.exception_handler import exception_msg


if __name__ == '__main__':
    logger = get_logger('test_query_gpu_request')
    logger.info('Begin to test API for querying local GPU infos')
    logger.info('Begin to send request to url: %s' % QUERY_GPU_TEST_URL)
    try:
        response = get(url=QUERY_GPU_TEST_URL)
        logger.info('Receive a response')
        logger.info('Response\'s status code: %s' % response.status_code)
        logger.info('Response\'s content: %s' % response.content)
    except StandardError as e:
        logger.error('Fail! Error message: %s\n' % exception_msg(e))
