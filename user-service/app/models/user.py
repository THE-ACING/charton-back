from app.models import Base

from sqlalchemy.orm import Mapped


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]
    photo_url: Mapped[str]
