# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 28/02/18 上午 11:41
from imdb import IMDB


class CocoFormatImdb(IMDB):
    def __init__(self, name):
        super(CocoFormatImdb, self).__init__(name=name)
