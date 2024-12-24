import asyncio
import logging
from uuid import UUID

import grpc  # type: ignore
import logfire
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, GrpcioProvider, DishkaAioInterceptor
from grpc_health.v1 import health  # type: ignore
from grpc_health.v1._async import _health_pb2_grpc  # type: ignore
from grpc_interceptor.exceptions import NotFound
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.database import DatabaseProvider
from app.models import User
from app.repositories.user import UserRepository
from app.settings import SettingsProvider
from app.utils import GrpcProvider
from services.user import user_pb2, user_pb2_grpc
from services.playlist import playlist_pb2_grpc, playlist_pb2


class UserMapper:
    @staticmethod
    def to_user_response(user: User) -> user_pb2.UserResponse:
        return user_pb2.UserResponse(
            id=str(user.id),
            username=user.username,
            photo_url=user.photo_url
        )

    @staticmethod
    def to_users_response(users: list[User]) -> user_pb2.UsersResponse:
        return user_pb2.UsersResponse(
            users=[UserMapper.to_user_response(user) for user in users]
        )


class UserServicer(user_pb2_grpc.UserServicer):
    @inject
    async def CreateUser(
        self,
        request: user_pb2.CreateUserRequest,
        context: grpc.aio.ServicerContext,
        user_repository: FromDishka[UserRepository],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
        session: FromDishka[AsyncSession],
    ) -> user_pb2.UserResponse:
        user = await user_repository.create(User(
            username=request.username,
            photo_url=request.photo_url
        ))
        await session.commit()

        await playlist_service.CreatePlaylist(
            playlist_pb2.CreatePlaylistRequest(
                title="Liked",
                is_liked=True
            ),
            metadata=(("user_id", str(user.id)),)
        )

        return UserMapper.to_user_response(user)

    @inject
    async def GetUser(  # type: ignore[override]
        self,
        request: user_pb2.UserRequest,
        context: grpc.aio.ServicerContext,
        user_repository: FromDishka[UserRepository],
    ) -> user_pb2.UserResponse:
        user = await user_repository.get(UUID(request.id))
        if user is None:
            raise NotFound("User not found")
        return UserMapper.to_user_response(user)

    @inject
    async def DeleteUser(  # type: ignore[override]
        self,
        request: user_pb2.UserRequest,
        context: grpc.aio.ServicerContext,
        user_repository: FromDishka[UserRepository],
        session: FromDishka[AsyncSession],
    ) -> user_pb2.UserResponse:
        user = await user_repository.get(UUID(request.id))
        if user is None:
            raise NotFound("User not found")

        await user_repository.delete(User.id == user.id)
        await session.commit()
        return UserMapper.to_user_response(user)

    @inject
    async def GetUsers(  # type: ignore[override]
        self,
        request: user_pb2.UsersRequest,
        context: grpc.aio.ServicerContext,
        user_repository: FromDishka[UserRepository],
    ) -> user_pb2.UsersResponse:
        users = await user_repository.find(limit=request.limit, offset=request.offset)
        return UserMapper.to_users_response(users)


async def serve() -> None:
    service_provider = Provider(scope=Scope.REQUEST)
    service_provider.provide(UserRepository)
    container = make_async_container(
        service_provider, SettingsProvider(), DatabaseProvider(), GrpcioProvider(), GrpcProvider()
    )

    logfire.configure(service_name="user-service")

    logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
    logfire.instrument_sqlalchemy(engine=(await container.get(AsyncEngine)).sync_engine)
    logfire.instrument_asyncpg()

    server = grpc.aio.server(interceptors=[DishkaAioInterceptor(container)])
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    _health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
