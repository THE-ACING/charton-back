from typing import List, TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import expression

from app.models import Base
if TYPE_CHECKING:
    from app.models.playlist_track import PlaylistTrack


class Playlist(Base):
    __tablename__ = "playlists"

    title: Mapped[str]
    thumbnail: Mapped[Optional[str]]

    is_liked: Mapped[bool] = mapped_column(default=False, server_default=expression.false())

    user_id: Mapped[UUID]

    tracks: Mapped[List["PlaylistTrack"]] = relationship(back_populates="playlist")
