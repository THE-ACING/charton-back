from dishka import Provider, Scope, provide
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str = Field(default=...)
    POSTGRES_PORT: int = Field(default=...)
    POSTGRES_USER: str = Field(default=...)
    POSTGRES_PASSWORD: SecretStr = Field(default=...)
    POSTGRES_DB: str = "user_service"

    PLAYLIST_SERVICE_GRPC_HOST: str = Field(default=...)
    PLAYLIST_SERVICE_GRPC_PORT: int = Field(default=...)

    model_config = SettingsConfigDict(env_file=("stack.env", ".env"), extra="ignore")


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()
