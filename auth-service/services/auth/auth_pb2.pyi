from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InitDataRequest(_message.Message):
    __slots__ = ("init_data",)
    INIT_DATA_FIELD_NUMBER: _ClassVar[int]
    init_data: str
    def __init__(self, init_data: _Optional[str] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = ("id", "username", "photo_url")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PHOTO_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    username: str
    photo_url: str
    def __init__(self, id: _Optional[str] = ..., username: _Optional[str] = ..., photo_url: _Optional[str] = ...) -> None: ...
