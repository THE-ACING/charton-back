# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: services/track/track.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'services/track/track.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1aservices/track/track.proto\x12\x05track\"2\n\x06\x41uthor\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0e\n\x06genres\x18\x03 \x01(\t\"l\n\x12\x43reateTrackRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x12\n\nauthor_ids\x18\x02 \x03(\t\x12\x10\n\x08\x64uration\x18\x03 \x01(\r\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x11\n\tthumbnail\x18\x05 \x01(\t\"\x1a\n\x0cTrackRequest\x12\n\n\x02id\x18\x01 \x01(\t\"\x7f\n\rTrackResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x1e\n\x07\x61uthors\x18\x03 \x03(\x0b\x32\r.track.Author\x12\x10\n\x08\x64uration\x18\x04 \x01(\r\x12\x0e\n\x06source\x18\x05 \x01(\t\x12\x11\n\tthumbnail\x18\x06 \x01(\t\".\n\rTracksRequest\x12\r\n\x05limit\x18\x01 \x01(\r\x12\x0e\n\x06offset\x18\x02 \x01(\r\"!\n\x12TracksByIdsRequest\x12\x0b\n\x03ids\x18\x01 \x03(\t\"6\n\x0eTracksResponse\x12$\n\x06tracks\x18\x01 \x03(\x0b\x32\x14.track.TrackResponse\"=\n\rSearchRequest\x12\r\n\x05query\x18\x01 \x01(\t\x12\r\n\x05limit\x18\x02 \x01(\r\x12\x0e\n\x06offset\x18\x03 \x01(\r\"3\n\x13\x43reateAuthorRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06genres\x18\x02 \x01(\t2\x80\x03\n\x05Track\x12@\n\x0b\x43reateTrack\x12\x19.track.CreateTrackRequest\x1a\x14.track.TrackResponse\"\x00\x12\x37\n\x08GetTrack\x12\x13.track.TrackRequest\x1a\x14.track.TrackResponse\"\x00\x12:\n\tGetTracks\x12\x14.track.TracksRequest\x1a\x15.track.TracksResponse\"\x00\x12\x44\n\x0eGetTracksByIds\x12\x19.track.TracksByIdsRequest\x1a\x15.track.TracksResponse\"\x00\x12=\n\x0cSearchTracks\x12\x14.track.SearchRequest\x1a\x15.track.TracksResponse\"\x00\x12;\n\x0c\x43reateAuthor\x12\x1a.track.CreateAuthorRequest\x1a\r.track.Author\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'services.track.track_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AUTHOR']._serialized_start=37
  _globals['_AUTHOR']._serialized_end=87
  _globals['_CREATETRACKREQUEST']._serialized_start=89
  _globals['_CREATETRACKREQUEST']._serialized_end=197
  _globals['_TRACKREQUEST']._serialized_start=199
  _globals['_TRACKREQUEST']._serialized_end=225
  _globals['_TRACKRESPONSE']._serialized_start=227
  _globals['_TRACKRESPONSE']._serialized_end=354
  _globals['_TRACKSREQUEST']._serialized_start=356
  _globals['_TRACKSREQUEST']._serialized_end=402
  _globals['_TRACKSBYIDSREQUEST']._serialized_start=404
  _globals['_TRACKSBYIDSREQUEST']._serialized_end=437
  _globals['_TRACKSRESPONSE']._serialized_start=439
  _globals['_TRACKSRESPONSE']._serialized_end=493
  _globals['_SEARCHREQUEST']._serialized_start=495
  _globals['_SEARCHREQUEST']._serialized_end=556
  _globals['_CREATEAUTHORREQUEST']._serialized_start=558
  _globals['_CREATEAUTHORREQUEST']._serialized_end=609
  _globals['_TRACK']._serialized_start=612
  _globals['_TRACK']._serialized_end=996
# @@protoc_insertion_point(module_scope)
