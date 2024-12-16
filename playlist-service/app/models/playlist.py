from typing import List, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.orm import Mapped, relationship

from app.models import Base
if TYPE_CHECKING:
    from app.models.playlist_track import PlaylistTrack


class Playlist(Base):
    __tablename__ = "playlists"

    title: Mapped[str]
    thumbnail: Mapped[str]

    user_id: Mapped[UUID]

    tracks: Mapped[List["PlaylistTrack"]] = relationship(back_populates="playlist")