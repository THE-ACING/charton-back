from typing import AsyncIterable

import grpc
from b2sdk.v2 import InMemoryAccountInfo, B2Api, Bucket
from dishka import Provider, provide, Scope

from app.settings import Settings
from services.user import user_pb2_grpc


class GrpcProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_user_service(self, settings: Settings) -> AsyncIterable[user_pb2_grpc.UserStub]:
        async with grpc.aio.insecure_channel(f'{settings.USER_SERVICE_GRPC_HOST}:{settings.USER_SERVICE_GRPC_PORT}') as channel:
            yield user_pb2_grpc.UserStub(channel)


class B2SDKProvider(Provider):
    @provide(scope=Scope.APP)
    def get_b2_sdk(self, settings: Settings) -> B2Api:
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", settings.B2_KEY_ID, settings.B2_APPLICATION_KEY)
        return b2_api

    @provide(scope=Scope.APP)
    def get_photos_bucket(self, b2_sdk: B2Api, settings: Settings) -> Bucket:
        return b2_sdk.get_bucket_by_name(settings.B2_PHOTOS_BUCKET_NAME)
