@echo off
protoc -I=./ --java_out=../frontend/src ./mxboard.proto