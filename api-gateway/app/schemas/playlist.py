from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.tracks import Track


class CreatePlaylist(BaseModel):
    title: str
    thumbnail: Optional[str] = None


class Playlist(CreatePlaylist):
    id: UUID
    is_liked: bool = False


class PlaylistWithTracks(Playlist):
    tracks: List[Track]


class Playlists(BaseModel):
    playlists: List[Playlist]
