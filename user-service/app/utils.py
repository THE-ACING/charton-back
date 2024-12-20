from typing import AsyncIterable

import grpc
from dishka import Provider, provide, Scope

from app.settings import Settings
from services.playlist import playlist_pb2_grpc


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_playlist_service(self, settings: Settings) -> AsyncIterable[playlist_pb2_grpc.PlaylistStub]:
        async with grpc.aio.insecure_channel(f'{settings.PLAYLIST_SERVICE_GRPC_HOST}:{settings.PLAYLIST_SERVICE_GRPC_PORT}') as channel:
            yield playlist_pb2_grpc.PlaylistStub(channel)