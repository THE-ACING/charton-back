from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base, TimestampMixin
if TYPE_CHECKING:
    from app.models.author import Author


class Track(TimestampMixin, Base):
    __tablename__ = "tracks"

    title: Mapped[str]
    authors: Mapped[List['Author']] = relationship(secondary="track_authors", back_populates="tracks")
    duration: Mapped[int]
    source: Mapped[str]
    thumbnail: Mapped[str]


