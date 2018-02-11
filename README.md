# MXServer

`MXServer` is a training/testing `Http/RPC` interface for [MXNet](https://github.com/apache/incubator-mxnet)
(currently based `mxnet-0.11.0`). And it is designed to support `image classification` and `object detection` 
training/test task right now. After I finish the basic parts, I will consider to make it possible to support other deep
learning tasks.

## 1. How to Use

## 2. Architecture

### 2.1 General Architecture

![](https://github.com/Harmonicahappy/mxboard/blob/master/GeneralArchitecture.PNG)

### 2.2 Backend Architecture

![](https://github.com/Harmonicahappy/mxboard/blob/master/BackendArchitecture.PNG)

## 3. Open APIs

In my original design, the mxboard will have open APIs in the form of `flask webservice`. I design roughly 3 interfaces.

### 3.1 train

* URL: `http://ip_address:5000/train`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to *example_task_desc.json* in folder proto
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "OK_TO_RUN"}`

### 3.2 predict

* URL: `http://ip_address:5000/predict`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to *example_task_desc.json* in folder proto
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "OK_TO_RUN"}`

### 3.3 stop

* URL: `http://ip_address:5000/stop`
* Method: `POST`
* Param type: `JSON`
* Param example: `{"task_id": "19700101"}`
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "STOP_SUCCESSFULLY"}`

### 3.4 query local gpu info

* URL: `http://ip_address:5000/gpu`
* Method: `GET`
* Param: `No param`
* Return type: `JSON`
* Return example(Success): `[{"free_mem": "8154316800", "used_mem": "378404864", "total_mem": "8532721664", "device_id": "0"}]`
* Return example(Failure): `[]`

## 4. Thirdparty Dependency

### 4.1 Python Thirdparty Dependency

* [MXNet and its dependencies](https://github.com/apache/incubator-mxnet)
* grpc and its dependencies
* nvidia-ml-py
* Flask
* pymongo
* kazoo

### 5. TODOs

* Data prepare for object detection

* Sub class of `Executor` for object detection
