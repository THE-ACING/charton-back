# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: services/user/user.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'services/user/user.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18services/user/user.proto\x12\x04user\"\x19\n\x0bUserRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x13\n\x11\x43reateUserRequest\"\x1a\n\x0cUserResponse\x12\n\n\x02id\x18\x01 \x01(\t\"-\n\x0cUsersRequest\x12\r\n\x05limit\x18\x01 \x01(\r\x12\x0e\n\x06offset\x18\x02 \x01(\r\"2\n\rUsersResponse\x12!\n\x05users\x18\x01 \x03(\x0b\x32\x12.user.UserResponse2\xe5\x01\n\x04User\x12\x32\n\x07GetUser\x12\x11.user.UserRequest\x1a\x12.user.UserResponse\"\x00\x12;\n\nCreateUser\x12\x17.user.CreateUserRequest\x1a\x12.user.UserResponse\"\x00\x12\x35\n\nDeleteUser\x12\x11.user.UserRequest\x1a\x12.user.UserResponse\"\x00\x12\x35\n\x08GetUsers\x12\x12.user.UsersRequest\x1a\x13.user.UsersResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.user.user_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERREQUEST']._serialized_start=34
  _globals['_USERREQUEST']._serialized_end=59
  _globals['_CREATEUSERREQUEST']._serialized_start=61
  _globals['_CREATEUSERREQUEST']._serialized_end=80
  _globals['_USERRESPONSE']._serialized_start=82
  _globals['_USERRESPONSE']._serialized_end=108
  _globals['_USERSREQUEST']._serialized_start=110
  _globals['_USERSREQUEST']._serialized_end=155
  _globals['_USERSRESPONSE']._serialized_start=157
  _globals['_USERSRESPONSE']._serialized_end=207
  _globals['_USER']._serialized_start=210
  _globals['_USER']._serialized_end=439
# @@protoc_insertion_point(module_scope)