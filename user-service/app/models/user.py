from typing import Optional
from uuid import UUID

from app.models import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    photo_url: Mapped[str]

    referrer_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"))
