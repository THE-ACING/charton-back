from typing import AsyncIterable

from dishka import provide, Provider, Scope
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from app.settings import Settings


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def get_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(
            URL.create(
                "postgresql+asyncpg",
                username=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD.get_secret_value(),
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
            )
        )

    @provide(scope=Scope.APP)
    def get_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session