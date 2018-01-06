# MXBoard

MXBoard is the training/testing visualization user interface for [MXNet](https://github.com/apache/incubator-mxnet)
(currently based `mxnet-0.11.0`). And it is designed to support `image classification` and `object detection` 
training/test task now. After I finish the basic parts, I will consider to make it possible to support other deep 
learning tasks.

## 1. How to Use

## 2. Architecture

### 2.1 General Architecture

![](https://github.com/Harmonicahappy/mxboard/tree/master/imgs/GeneralArchitecture.PNG)

## 3. Open APIs

In my original design, the mxboard will have open APIs in the form of `flask webservice`. I design roughly 3 interfaces.

### 3.1 train

* URL: `ip_address:5000/train`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to *example_task_desc.json* in folder proto
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "OK_TO_RUN"}`

### 3.2 predict

* URL: `ip_address:5000/predict`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to *example_task_desc.json* in folder proto
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "OK_TO_RUN"}`

### 3.3 stop

* URL: `ip_address:5000/stop`
* Method: `POST`
* Param type: `JSON`
* Param example: `{"task_id": "19700101"}`
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "STOP_SUCCESSFULLY"}`

## 4. Thirdparty Dependency

### 4.1 Java Thirdparty Dependency

### 4.2 Python Thirdparty Dependency
