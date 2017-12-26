# -*- coding: utf-8 -*-

# ------------------------------
# Copyright (c) 2017 Terence Wu
# ------------------------------
import json

from backend.mxboard.util.xml_parser import mxboard_storage_config
from mxnet import symbol as sym


def create_symbol(symbol_name, net_define_json):
    symbol = None
    try:
        net_definition = json.loads(net_define_json)
        for component in net_definition:
            if component['type'] == 'Input':
                component_name = component['name']
                symbol = sym.Variable(component_name)
        symbol_json_store_root = mxboard_storage_config['symbol-json-root']
        symbol_store_path = symbol_json_store_root + symbol_name
        symbol.save(fname=symbol_store_path)
        return symbol_store_path
    except StandardError:
        return None

