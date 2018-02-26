# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:37
from config import FLASK_PORT

TEST_BASE_URL = 'http://127.0.0.1:%s' % FLASK_PORT
TRAIN_TEST_URL = TEST_BASE_URL + '/train'
INFERENCE_TEST_URL = TEST_BASE_URL + '/test'
STOP_TEST_URL = TEST_BASE_URL + '/stop'
QUERY_GPU_TEST_URL = TEST_BASE_URL + '/gpu'

TRAIN_REQUEST_JSON = {

}

TEST_REQUEST_JSON = {

}

STOP_REQUEST_JSON = {

}
