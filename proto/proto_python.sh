#!/usr/bin/env bash

python -m grpc_tools.protoc -I. --python_out=../worker/proto/ --grpc_python_out=../worker/proto/ ./mxserver.proto