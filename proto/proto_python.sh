#!/usr/bin/env bash

python -m grpc_tools.protoc -I. --python_out=../backend/mxboard/proto/ --grpc_python_out=../backend/mxboard/proto/ ./mxboard.proto