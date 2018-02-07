# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 下午 02:42
from ctypes import c_int, c_longlong, Structure
from worker.mx.util.xml_parser import mxserver_gpu_config

LOCAL_GPU_NUM = mxserver_gpu_config['gpu-num']


class GpuMemory(Structure):
    _fields_ = [
        ('total', c_longlong),
        ('used', c_longlong),
        ('free', c_longlong)
    ]


GPU_ARRAY = LOCAL_GPU_NUM * GpuMemory


class GpuInfos(Structure):
    __fields_ = [
        ('gpu_num', c_int),
        ('gpus', GPU_ARRAY)
    ]
