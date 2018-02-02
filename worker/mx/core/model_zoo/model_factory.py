# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 15/01/18 下午 01:33
from worker.mx.core.model_zoo import alexnet, vgg, inception, resnet, densenet, faster_rcnn

registered_model = {
    'alexnet': alexnet.alexnet,
    'vgg': vgg.vgg,
    'inception': inception,
    'resnet': resnet.resnet,
    'densenet': densenet.densenet,
    'faster_rcnn': faster_rcnn.faster_rcnn
}


def get_symbol(name, config=None):
    func = registered_model.get(name)
    if func:
        return func(config)
