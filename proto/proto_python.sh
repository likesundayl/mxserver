#!/usr/bin/env bash

python -m grpc_tools.protoc -I. --python_out=../worker/mx/proto/ --grpc_python_out=../worker/mx/proto/ ./mxserver.proto