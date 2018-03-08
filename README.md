# MXServer

`MXServer` is a training/testing `Http/RPC` interface for [MXNet](https://github.com/apache/incubator-mxnet)
(currently based `mxnet-0.11.0`). And it is designed to support `image classification` and `object detection` 
training/test task right now. After I finish the basic parts, I will consider to make it possible to support other deep
learning tasks. 

In `MXServer`, the training/testing logs/results will be stored in `MongoDB`, you can export or query them through `task_id` 
by send a query request to `MongoDB`. `MXServer` can be integrated with `ZooKeeper` in distribution environment, these 
features are useful when integrate `MXServer` with traditional Web development(I will consider to put logs/results to 
`Message Queue` plugins such as `Kafka`). Besides, all your action will be stored, for example, if you start a `image 
classification` training task via `MXServer`, the hyper parameters, the datasets, the net, all these infos will be stored 
in local `MongoDB`, and you can query them and find best combination through comparing those experiments' settings.

## 1. How to Use

### 1.1 Download Source Codes
Clone source codes to your computer and extract it. Assume the extracted path is `MXSERVER_HOME`.

```bash
git clone https://github.com/Harmonicahappy/mxserver.git
```

### 1.2 Modify config file

Find `config.py`, it is in `MXSERVER_HOME`, open it by any editor. Modify following things:

* `MXSERVER_HOME`: Line 12, change its value to the root path of your extracted `mxserver`

* `RCNN_PACKAGE`: Line 22, change it to your rcnn package's path of `MXNet`

* `MONGO_HOST` & `MONGO_PORT`: Line 27 & line 28, change them according to your own config

* `RPC_HOST` & `RPC_PORT`: Line 37 & line 38, change them according to your own config

* `ZooKeeper config`: Line 51 to 53, change them according to your own config

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

## 3. Flask Restful APIs

### 3.1 train

* URL: `http://ip_address:5000/train`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to field: `TRAIN_REQUEST_JSON` in *test_resources.py* in folder test
* Return type: `JSON`
* Return example: `{"task_id": "19700101", "state_code": "0", "state_desc": "OK_TO_RUN"}`

### 3.2 evaluation

* URL: `http://ip_address:5000/eval`
* Method: `POST`
* Param type: `JSON`
* Param example: please refer to field: `TEST_REQUEST_JSON` in *test_resources.py* in folder test
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

## 4. Runtime Mode

### 4.1 Single machine for flask server and worker server

In this mode, both flask server and worker server will be running on the same machine, it is suitable for personal use.

### 4.2 Single machine for flask server, multi-machine for worker server

This mode is a typical distribution system, service registry and discovery will be accomplished via `ZooKeeper`. Once there
is a request to start a deep learning task, the dispatcher in flask server will find all available workers via `ZooKeeper` and choose a 
worker and assign the task to it according to each worker's `GPU` info.

## 5. Thirdparty Dependency

* [MXNet and its dependencies](https://github.com/apache/incubator-mxnet)
* grpc and its dependencies
* nvidia-ml-py
* Flask
* pymongo
* kazoo

### 6. TODOs

* 2018-03-08: I decide to redesign some parts of worker

* Release a beta version before the end of March.

* Data prepare for object detection

* Sub class of `Executor` for object detection
