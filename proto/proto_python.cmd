python -m grpc_tools.protoc -I. --python_out=../worker/mx/proto/ --grpc_python_out=../worker/mx/proto/ ./mxboard.proto
pause