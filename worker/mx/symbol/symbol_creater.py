# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import json

import os

from mxnet import symbol as sym

from worker.mx.util.xml_parser import mxserver_storage_config


def create_symbol(symbol_name, net_define_json):
    symbol = None
    try:
        net_definition = json.loads(net_define_json)
        for component in net_definition:
            if component['type'] == 'Input':
                component_name = component['name']
                symbol = sym.Variable(component_name)
        symbol_json_store_root = mxserver_storage_config['symbol-json-root']
        if not os.path.exists(symbol_json_store_root):
            os.mkdir(symbol_json_store_root)
        symbol_store_path = symbol_json_store_root + symbol_name
        symbol.save(fname=symbol_store_path)
        return symbol_store_path
    except StandardError:
        return None
