from dishka import provide, Provider, Scope
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TRACK_SERVICE_GRPC_HOST: str = Field(default=...)
    TRACK_SERVICE_GRPC_PORT: int = Field(default=...)

    AUTH_SERVICE_GRPC_HOST: str = Field(default=...)
    AUTH_SERVICE_GRPC_PORT: int = Field(default=...)

    PLAYLIST_SERVICE_GRPC_HOST: str = Field(default=...)
    PLAYLIST_SERVICE_GRPC_PORT: int = Field(default=...)

    USER_SERVICE_GRPC_HOST: str = Field(default=...)
    USER_SERVICE_GRPC_PORT: int = Field(default=...)

    model_config = SettingsConfigDict(
        env_file=('stack.env', '.env'),
        extra="ignore"
    )


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()
