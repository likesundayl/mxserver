# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mxboard.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mxboard.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\rmxboard.proto\"$\n\rTaskParameter\x12\x13\n\x02id\x18\x01 \x02(\x0b\x32\x07.TaskId\"\x19\n\x06TaskId\x12\x0f\n\x07task_id\x18\x01 \x02(\t\"A\n\tTaskState\x12\x15\n\nstate_code\x18\x01 \x02(\x05:\x01\x30\x12\x1d\n\nstate_desc\x18\x02 \x02(\t:\tOK_TO_RUN2\\\n\x0cMXNetService\x12)\n\tstartTask\x12\x0e.TaskParameter\x1a\n.TaskState\"\x00\x12!\n\x08stopTask\x12\x07.TaskId\x1a\n.TaskState\"\x00')
)




_TASKPARAMETER = _descriptor.Descriptor(
  name='TaskParameter',
  full_name='TaskParameter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='TaskParameter.id', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=53,
)


_TASKID = _descriptor.Descriptor(
  name='TaskId',
  full_name='TaskId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='TaskId.task_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=55,
  serialized_end=80,
)


_TASKSTATE = _descriptor.Descriptor(
  name='TaskState',
  full_name='TaskState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state_code', full_name='TaskState.state_code', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='state_desc', full_name='TaskState.state_desc', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=True, default_value=_b("OK_TO_RUN").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=82,
  serialized_end=147,
)

_TASKPARAMETER.fields_by_name['id'].message_type = _TASKID
DESCRIPTOR.message_types_by_name['TaskParameter'] = _TASKPARAMETER
DESCRIPTOR.message_types_by_name['TaskId'] = _TASKID
DESCRIPTOR.message_types_by_name['TaskState'] = _TASKSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskParameter = _reflection.GeneratedProtocolMessageType('TaskParameter', (_message.Message,), dict(
  DESCRIPTOR = _TASKPARAMETER,
  __module__ = 'mxboard_pb2'
  # @@protoc_insertion_point(class_scope:TaskParameter)
  ))
_sym_db.RegisterMessage(TaskParameter)

TaskId = _reflection.GeneratedProtocolMessageType('TaskId', (_message.Message,), dict(
  DESCRIPTOR = _TASKID,
  __module__ = 'mxboard_pb2'
  # @@protoc_insertion_point(class_scope:TaskId)
  ))
_sym_db.RegisterMessage(TaskId)

TaskState = _reflection.GeneratedProtocolMessageType('TaskState', (_message.Message,), dict(
  DESCRIPTOR = _TASKSTATE,
  __module__ = 'mxboard_pb2'
  # @@protoc_insertion_point(class_scope:TaskState)
  ))
_sym_db.RegisterMessage(TaskState)



_MXNETSERVICE = _descriptor.ServiceDescriptor(
  name='MXNetService',
  full_name='MXNetService',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=149,
  serialized_end=241,
  methods=[
  _descriptor.MethodDescriptor(
    name='startTask',
    full_name='MXNetService.startTask',
    index=0,
    containing_service=None,
    input_type=_TASKPARAMETER,
    output_type=_TASKSTATE,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='stopTask',
    full_name='MXNetService.stopTask',
    index=1,
    containing_service=None,
    input_type=_TASKID,
    output_type=_TASKSTATE,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_MXNETSERVICE)

DESCRIPTOR.services_by_name['MXNetService'] = _MXNETSERVICE

# @@protoc_insertion_point(module_scope)
