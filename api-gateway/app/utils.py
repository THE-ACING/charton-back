from typing import AsyncIterable

import grpc
from dishka import Provider, provide, Scope

from app.settings import Settings
from services.playlist import playlist_pb2_grpc
from services.track import track_pb2_grpc
from services.auth import auth_pb2_grpc
from services.user import user_pb2_grpc


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_track_service(self, settings: Settings) -> AsyncIterable[track_pb2_grpc.TrackStub]:
        async with grpc.aio.insecure_channel(f'{settings.TRACK_SERVICE_GRPC_HOST}:{settings.TRACK_SERVICE_GRPC_PORT}') as channel:
            yield track_pb2_grpc.TrackStub(channel)

    @provide(scope=Scope.APP)
    async def get_auth_service(self, settings: Settings) -> AsyncIterable[auth_pb2_grpc.AuthStub]:
        async with grpc.aio.insecure_channel(f'{settings.AUTH_SERVICE_GRPC_HOST}:{settings.AUTH_SERVICE_GRPC_PORT}') as channel:
            yield auth_pb2_grpc.AuthStub(channel)

    @provide(scope=Scope.APP)
    async def get_playlist_service(self, settings: Settings) -> AsyncIterable[playlist_pb2_grpc.PlaylistStub]:
        async with grpc.aio.insecure_channel(f'{settings.PLAYLIST_SERVICE_GRPC_HOST}:{settings.PLAYLIST_SERVICE_GRPC_PORT}') as channel:
            yield playlist_pb2_grpc.PlaylistStub(channel)

    @provide(scope=Scope.APP)
    async def get_user_service(self, settings: Settings) -> AsyncIterable[user_pb2_grpc.UserStub]:
        async with grpc.aio.insecure_channel(f'{settings.USER_SERVICE_GRPC_HOST}:{settings.USER_SERVICE_GRPC_PORT}') as channel:
            yield playlist_pb2_grpc.PlaylistStub(channel)