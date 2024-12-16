from sqlalchemy.ext.asyncio import AsyncSession

from app.models import TelegramUser
from app.repositories.base import BaseRepository


class TelegramUserRepository(BaseRepository[TelegramUser]):
    def __init__(self, session: AsyncSession):
        super().__init__(TelegramUser, session)
