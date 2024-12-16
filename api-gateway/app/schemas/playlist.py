from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Track(BaseModel):
    id: UUID


class CreatePlaylist(BaseModel):
    title: str
    thumbnail: Optional[str] = None


class Playlist(CreatePlaylist):
    id: UUID


class PlaylistWithTracks(Playlist):
    tracks: list[Track]


class Playlists(BaseModel):
    playlists: list[Playlist]
