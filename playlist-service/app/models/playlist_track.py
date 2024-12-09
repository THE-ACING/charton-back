from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models import Base
if TYPE_CHECKING:
    from app.models.playlist import Playlist


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"

    track_id: Mapped[UUID]

    playlist_id: Mapped[UUID] = mapped_column(foreign_key="playlists.id")
    playlist: Mapped[Playlist] = relationship(back_populates="tracks")

    __table_args__ = (
        UniqueConstraint("track_id", "playlist_id"),
    )


