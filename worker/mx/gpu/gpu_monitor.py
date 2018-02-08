# -*- coding: utf-8 -*-

# @Author: Terence Wu
# @Time: 07/02/18 下午 02:42
from json import dumps
from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo


def query_gpu():
    """
    Query local GPU information via `pynvml`(`nvml` is installed when CUDA is installed)
    :return:
    """
    local_gpu_infos = []
    nvmlInit()
    device_count = nvmlDeviceGetCount()

    for i in range(device_count):
        handle = nvmlDeviceGetHandleByIndex(i)
        gpu_mem_info = nvmlDeviceGetMemoryInfo(handle)
        local_gpu_infos.append({"device_id": "%s" % (i + 1), "total_mem": "%s" % gpu_mem_info.total,
                                "used_mem": "%s" % gpu_mem_info.used, "free_mem": "%s" % gpu_mem_info.free})

    return dumps(local_gpu_infos)
