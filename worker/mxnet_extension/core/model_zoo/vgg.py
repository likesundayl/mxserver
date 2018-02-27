# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 15/01/18 下午 01:22
import mxnet as mx
import numpy as np

# MXNet's LICENSE
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


def get_internal_layers(internel_layer, layers, filters, batch_norm=False):
    for i, num in enumerate(layers):
        for j in range(num):
            internel_layer = mx.sym.Convolution(data=internel_layer, kernel=(3, 3), pad=(1, 1), num_filter=filters[i],
                                                name="conv%s_%s" % (i + 1, j + 1))
            if batch_norm:
                internel_layer = mx.symbol.BatchNorm(data=internel_layer, name="bn%s_%s" % (i + 1, j + 1))
            internel_layer = mx.sym.Activation(data=internel_layer, act_type="relu", name="relu%s_%s" % (i + 1, j + 1))
        internel_layer = mx.sym.Pooling(data=internel_layer, pool_type="max", kernel=(2, 2), stride=(2, 2),
                                        name="pool%s" % (i + 1))
    return internel_layer


def get_classifier_layers(bottom, num_classes):
    flatten = mx.sym.Flatten(data=bottom, name="flatten")
    fc6 = mx.sym.FullyConnected(data=flatten, num_hidden=4096, name="fc6")
    relu6 = mx.sym.Activation(data=fc6, act_type="relu", name="relu6")
    drop6 = mx.sym.Dropout(data=relu6, p=0.5, name="drop6")
    fc7 = mx.sym.FullyConnected(data=drop6, num_hidden=4096, name="fc7")
    relu7 = mx.sym.Activation(data=fc7, act_type="relu", name="relu7")
    drop7 = mx.sym.Dropout(data=relu7, p=0.5, name="drop7")
    fc8 = mx.sym.FullyConnected(data=drop7, num_hidden=num_classes, name="fc8")
    return fc8


def vgg(config):
    num_layers = config['num_layer']
    num_classes = config['num_classes']
    use_batch_norm = True if config['bn'] == '0' else False
    dtype = 'float32'
    if config.get('dtype'):
        dtype = config['dtype']

    vgg_spec = {11: ([1, 1, 2, 2, 2], [64, 128, 256, 512, 512]),
                13: ([2, 2, 2, 2, 2], [64, 128, 256, 512, 512]),
                16: ([2, 2, 3, 3, 3], [64, 128, 256, 512, 512]),
                19: ([2, 2, 4, 4, 4], [64, 128, 256, 512, 512])}
    if num_layers not in vgg_spec:
        num_layers = 16
    layers, filters = vgg_spec[num_layers]
    data = mx.sym.Variable(name="data")
    if dtype == 'float16':
        data = mx.sym.Cast(data=data, dtype=np.float16)
    feature = get_internal_layers(data, layers, filters, use_batch_norm)
    classifier = get_classifier_layers(feature, num_classes)
    if dtype == 'float16':
        classifier = mx.sym.Cast(data=classifier, dtype=np.float32)
    symbol = mx.sym.SoftmaxOutput(data=classifier, name='softmax')
    return symbol


