from typing import List
from uuid import UUID

from pydantic import BaseModel

from app.schemas.author import Author


class Track(BaseModel):
    id: UUID
    title: str
    authors: List[Author]

    duration: int
    source: str
    thumbnail: str


class Tracks(BaseModel):
    tracks: list[Track]