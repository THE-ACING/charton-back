from dishka import provide, Provider, Scope
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TRACK_SERVICE_GRPC_HOST: str
    TRACK_SERVICE_GRPC_PORT: int

    AUTH_SERVICE_GRPC_HOST: str
    AUTH_SERVICE_GRPC_PORT: int

    PLAYLIST_SERVICE_GRPC_HOST: str
    PLAYLIST_SERVICE_GRPC_PORT: int

    USER_SERVICE_GRPC_HOST: str
    USER_SERVICE_GRPC_PORT: int

    model_config = SettingsConfigDict(
        env_file=('stack.env', '.env'),
        extra="ignore"
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()
