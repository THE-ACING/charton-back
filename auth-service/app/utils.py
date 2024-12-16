from typing import AsyncIterable

import grpc
from dishka import Provider, provide, Scope

from app.settings import Settings
from services.user import user_pb2_grpc


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_user_service(self, settings: Settings) -> AsyncIterable[user_pb2_grpc.UserStub]:
        async with grpc.aio.insecure_channel(f'{settings.USER_SERVICE_GRPC_HOST}:{settings.USER_SERVICE_GRPC_PORT}') as channel:
            yield user_pb2_grpc.UserStub(channel)