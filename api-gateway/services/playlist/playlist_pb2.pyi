from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlaylistRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class CreatePlaylistRequest(_message.Message):
    __slots__ = ("title", "thumbnail")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    title: str
    thumbnail: str
    def __init__(self, title: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class UpdatePlaylistRequest(_message.Message):
    __slots__ = ("id", "title", "thumbnail")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    thumbnail: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class PlaylistResponse(_message.Message):
    __slots__ = ("id", "title", "thumbnail")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    thumbnail: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class TrackResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class PlaylistTracksResponse(_message.Message):
    __slots__ = ("id", "title", "thumbnail", "tracks")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    thumbnail: str
    tracks: _containers.RepeatedCompositeFieldContainer[TrackResponse]
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., thumbnail: _Optional[str] = ..., tracks: _Optional[_Iterable[_Union[TrackResponse, _Mapping]]] = ...) -> None: ...

class AddTrackToPlaylistRequest(_message.Message):
    __slots__ = ("playlist_id", "track_id")
    PLAYLIST_ID_FIELD_NUMBER: _ClassVar[int]
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    playlist_id: str
    track_id: str
    def __init__(self, playlist_id: _Optional[str] = ..., track_id: _Optional[str] = ...) -> None: ...

class PlaylistsRequest(_message.Message):
    __slots__ = ("limit", "offset")
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    limit: int
    offset: int
    def __init__(self, limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class UserPlaylistsRequest(_message.Message):
    __slots__ = ("user_id", "limit", "offset")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    limit: int
    offset: int
    def __init__(self, user_id: _Optional[str] = ..., limit: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class PlaylistsResponse(_message.Message):
    __slots__ = ("playlists",)
    PLAYLISTS_FIELD_NUMBER: _ClassVar[int]
    playlists: _containers.RepeatedCompositeFieldContainer[PlaylistResponse]
    def __init__(self, playlists: _Optional[_Iterable[_Union[PlaylistResponse, _Mapping]]] = ...) -> None: ...
