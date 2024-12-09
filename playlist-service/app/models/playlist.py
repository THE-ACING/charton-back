from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from app.models import Base
if TYPE_CHECKING:
    from app.models.playlist_track import PlaylistTrack


class Playlist(Base):
    title: Mapped[str]
    thumbnail: Mapped[str]

    tracks: Mapped[List["PlaylistTrack"]] = relationship(back_populates="playlist")