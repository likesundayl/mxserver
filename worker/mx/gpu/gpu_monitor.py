# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 下午 02:42
from ctypes import CDLL, RTLD_LOCAL
from os import name as osname, environ
from json import dumps


def query_gpu():
    """
    Query local GPU information via `nvml`(`nvml` is installed when CUDA is installed)
    :return:
    """
    local_gpu_infos = []

    return dumps(local_gpu_infos)


def load_nvml_lib():
    if osname == 'posix':
        return CDLL('libnvidia-ml.so', RTLD_LOCAL)
    if osname == 'nt':
        cuda_home = environ.get('CUDA_HOME')
