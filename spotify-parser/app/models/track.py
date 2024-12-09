from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.models.base import Base, TimestampMixin
if TYPE_CHECKING:
    from app.models.author import Author


class Track(TimestampMixin, Base):
    __tablename__ = "tracks"

    spotify_id: Mapped[str] = mapped_column(unique=True)

    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="tracks")

