
from dishka import Provider, Scope, provide
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str = "playlist_service"

    TRACK_SERVICE_GRPC_HOST: str
    TRACK_SERVICE_GRPC_PORT: int

    model_config = SettingsConfigDict(
        env_file=('stack.env', '.env'),
        extra="ignore"
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

