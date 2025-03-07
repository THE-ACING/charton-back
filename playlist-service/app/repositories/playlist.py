from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Playlist
from app.repositories.base import BaseRepository


class PlaylistRepository(BaseRepository[Playlist]):
    def __init__(self, session: AsyncSession):
        super().__init__(Playlist, session)
