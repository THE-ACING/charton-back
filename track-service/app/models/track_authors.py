from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class TrackAuthors(Base):
    __tablename__ = "track_authors"

    track_id: Mapped[UUID] = mapped_column(ForeignKey("tracks.id"))
    author_id: Mapped[UUID] = mapped_column(ForeignKey("authors.id"))

    __table_args__ = (
        UniqueConstraint("track_id", "author_id"),
    )