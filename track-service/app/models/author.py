from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.models import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models import Track


class Author(TimestampMixin, Base):
    __tablename__ = 'authors'

    name: Mapped[str]
    genres: Mapped[str]
    tracks: Mapped[List['Track']] = relationship(back_populates='author')