from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Track(BaseModel):
    id: Optional[UUID]
    title: str
    duration: int
    source: str
    thumbnail: str


class Tracks(BaseModel):
    tracks: list[Track]