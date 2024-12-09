from typing import AsyncIterable

import grpc
from dishka import Provider, provide, Scope

from app.settings import Settings
from services.track import track_pb2_grpc


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_track_service(self, settings: Settings) -> AsyncIterable[track_pb2_grpc.TrackStub]:
        async with grpc.aio.insecure_channel(f'{settings.TRACK_SERVICE_GRPC_HOST}:{settings.TRACK_SERVICE_GRPC_PORT}') as channel:
            yield track_pb2_grpc.TrackStub(channel)