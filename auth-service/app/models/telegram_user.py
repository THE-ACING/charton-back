from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class TelegramUser(Base):
    __tablename__ = "telegram_users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
