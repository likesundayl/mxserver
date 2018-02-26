# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 26/02/18 上午 11:36
from requests import post
from test_resources import TRAIN_TEST_URL, TRAIN_REQUEST_JSON


if __name__ == '__main__':
    response = post(url=TRAIN_TEST_URL, json=TRAIN_REQUEST_JSON)
