# MXServer

`MXServer` is a training/testing `Http/RPC` interface for [MXNet](https://github.com/apache/incubator-mxnet)
(currently based `mxnet-0.11.0`). And it is designed to support `image classification` and `object detection` 
training/test task right now. After I finish the basic parts, I will consider to make it possible to support other deep
learning tasks.

## 1. How to Use

### 1.1 Download Source Codes
Clone source codes to your computer and extract it. Assume the extracted path is `MXSERVER_HOME`.

```bash
git clone https://github.com/Harmonicahappy/mxserver.git
```

### 1.2 Modify config file

Find `config.py`, it is in `MXSERVER_HOME`, open it by any editor. Modify following things:

* `RCNN_PACKAGE`: Line 16, change it to your rcnn package's path of `MXNet`

* `MONGO_HOST` & `MONGO_PORT`: Line 21 & line 22, change them according to your own config

* `RPC_HOST` & `RPC_PORT`: Line 31 & line 32, change them according to your own config

* `ZooKeeper config`: Line 39 to 41, change them according to your own config

* `LOG_FILE_ROOT`: Line 46, change it to `MXSERVER_HOME/log/`

* `REC_ROOT`: Line 55, change it to `MXSERVER_HOME/data_center/`

* `SYMBOL_JSON_ROOT`: Line 56, change it to `MXSERVER_HOME/model_zoo/`

* `PARAMS_ROOT`: Line 57, change it to `MXSERVER_HOME/params_zoo/`

Of course, you can modify other fields in `config.py` if you are not satisfied with the default config.

### 1.3 Start RPC server and Flask server

Locate folder `bin` in `MXSERVER_HOME`

#### 1.3.1 Windows
Double click `start_worker_server.bat` and `start_flask_server.bat`

#### 1.3.2 Linux
Open terminal in `MXSERVER_HOME/bin`
```bash
sh ./start_worker_server.sh
```
Open another terminal in `MXSERVER_HOME/bin`
```bash
sh ./start_flask_server.sh
```

#### 1.4 Other

Don't forget to start `MongoDB` service, and if you want to use `ZooKeeper`, don't forget to start `ZooKeeper` service.

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

* Release an beta version before the end of March.

* Data prepare for object detection

* Sub class of `Executor` for object detection
