from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.models.base import Base, TimestampMixin
if TYPE_CHECKING:
    from app.models.author import Author


class Track(TimestampMixin, Base):
    __tablename__ = "tracks"

    title: Mapped[str]
    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"))
    author: Mapped['Author'] = relationship(back_populates="tracks")
    duration: Mapped[int]
    source: Mapped[str]
    thumbnail: Mapped[str]


