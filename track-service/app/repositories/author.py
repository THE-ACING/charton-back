from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Author
from app.repositories.base import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    def __init__(self, session: AsyncSession):
        super().__init__(Author, session)
