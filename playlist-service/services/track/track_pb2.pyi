from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Author(_message.Message):
    __slots__ = ("id", "name", "genres")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GENRES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    genres: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., genres: _Optional[str] = ...) -> None: ...

class CreateTrackRequest(_message.Message):
    __slots__ = ("title", "author_ids", "duration", "source", "thumbnail")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_IDS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    title: str
    author_ids: _containers.RepeatedScalarFieldContainer[str]
    duration: int
    source: str
    thumbnail: str
    def __init__(self, title: _Optional[str] = ..., author_ids: _Optional[_Iterable[str]] = ..., duration: _Optional[int] = ..., source: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class TrackRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TrackResponse(_message.Message):
    __slots__ = ("id", "title", "authors", "duration", "source", "thumbnail")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHORS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    authors: _containers.RepeatedCompositeFieldContainer[Author]
    duration: int
    source: str
    thumbnail: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., authors: _Optional[_Iterable[_Union[Author, _Mapping]]] = ..., duration: _Optional[int] = ..., source: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class TracksRequest(_message.Message):
    __slots__ = ("limit", "offset")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class TracksByIdsRequest(_message.Message):
    __slots__ = ("ids",)
    IDS_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ids: _Optional[_Iterable[str]] = ...) -> None: ...

class TracksResponse(_message.Message):
    __slots__ = ("tracks",)
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    tracks: _containers.RepeatedCompositeFieldContainer[TrackResponse]
    def __init__(self, tracks: _Optional[_Iterable[_Union[TrackResponse, _Mapping]]] = ...) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ("query", "limit", "offset")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    query: str
    limit: int
    offset: int
    def __init__(self, query: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class CreateAuthorRequest(_message.Message):
    __slots__ = ("name", "genres")
    NAME_FIELD_NUMBER: _ClassVar[int]
    GENRES_FIELD_NUMBER: _ClassVar[int]
    name: str
    genres: str
    def __init__(self, name: _Optional[str] = ..., genres: _Optional[str] = ...) -> None: ...

class AuthorResponse(_message.Message):
    __slots__ = ("id", "name", "genres")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GENRES_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    genres: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., genres: _Optional[str] = ...) -> None: ...
