from typing import List, TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models import Track


class Author(Base, TimestampMixin):
    __tablename__ = 'authors'

    spotify_id: Mapped[str] = mapped_column(unique=True)

    tracks: Mapped[List['Track']] = relationship(back_populates='author')
