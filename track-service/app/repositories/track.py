from typing import Any, Optional

from sqlalchemy import BinaryExpression, ColumnOperators, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Track
from app.repositories.base import BaseRepository


class TrackRepository(BaseRepository[Track]):
    def __init__(self, session: AsyncSession):
        super().__init__(Track, session)

    async def random(self, *expressions: BinaryExpression[Any] | ColumnOperators) -> Optional[Track]:
        query = select(self.__model__).order_by(func.random())

        query = self._set_filter(query, expressions)

        return (await self._session.scalars(query)).first()