from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    KAFKA_TOPIC: str = "spotify"
    KAFKA_BOOTSTRAP_SERVERS: List[str]

    TRACK_SERVICE_GRPC_HOST: str
    TRACK_SERVICE_GRPC_PORT: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str = "spotify_parser"

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: SecretStr

    B2_KEY_ID: str
    B2_APPLICATION_KEY: str
    B2_TRACK_BUCKET_NAME: str


    model_config = SettingsConfigDict(
        env_file=('stack.env', '.env'),
        extra="ignore"
    )


settings = Settings() # type: ignore
