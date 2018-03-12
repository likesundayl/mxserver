# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 12/03/18 上午 09:34
from requests import post
from config import FLASK_HOST, FLASK_PORT
from util.logger_generator import get_logger

DEPLOY_ID = ''

if __name__ == '__main__':
    logger = get_logger('classify_logger')
    url = 'http://%s:%s/classify' % FLASK_HOST, FLASK_PORT
