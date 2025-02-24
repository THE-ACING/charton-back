from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(
    URL.create(
        "postgresql+psycopg",
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD.get_secret_value(),
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        database=settings.POSTGRES_DB,
    ),
    pool_pre_ping=True
)
session_maker = sessionmaker(engine, expire_on_commit=False, autoflush=False)
