#!/usr/bin/env bash

protoc -I=./ --java_out=../frontend/src ./mxboard.proto