import asyncio
import logging
from uuid import UUID

import grpc
import logfire
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, GrpcioProvider, DishkaAioInterceptor
from grpc_health.v1 import health
from grpc_health.v1._async import _health_pb2_grpc  # noqa
from grpc_interceptor.exceptions import NotFound
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.database import DatabaseProvider
from app.models import User
from app.repositories.user import UserRepository
from app.settings import SettingsProvider
from services.user import user_pb2, user_pb2_grpc


class UserServicer(user_pb2_grpc.UserServicer):
    @inject
    async def CreateUser(self, request: user_pb2.CreateUserRequest, context: grpc.aio.ServicerContext, user_repository: FromDishka[UserRepository], session: FromDishka[AsyncSession]) -> user_pb2.UserResponse:
        user = await user_repository.create(User())
        await session.commit()
        return user_pb2.UserResponse(id=str(user.id))

    @inject
    async def GetUser(self, request: user_pb2.UserRequest, context: grpc.aio.ServicerContext, user_repository: FromDishka[UserRepository]) -> user_pb2.UserResponse:
        user = await user_repository.get(UUID(request.id))
        if user is None:
            raise NotFound("User not found")
        return user_pb2.UserResponse(id=str(user.id))

    @inject
    async def DeleteUser(self, request: user_pb2.UserRequest, context: grpc.aio.ServicerContext, user_repository: FromDishka[UserRepository], session: FromDishka[AsyncSession]) -> user_pb2.UserResponse:
        user = await user_repository.get(UUID(request.id))
        if user is None:
            raise NotFound("User not found")

        await user_repository.delete(user)
        await session.commit()
        return user_pb2.UserResponse(id=str(user.id))

    @inject
    async def GetUsers(self, request: user_pb2.UsersRequest, context: grpc.aio.ServicerContext, user_repository: FromDishka[UserRepository]) -> user_pb2.UsersResponse:
        users = await user_repository.find(limit=request.limit, offset=request.offset)
        return user_pb2.UsersResponse(users=[user_pb2.UserResponse(id=str(user.id)) for user in users])



async def serve() -> None:
    service_provider = Provider(scope=Scope.REQUEST)
    service_provider.provide(UserRepository)
    container = make_async_container(service_provider, SettingsProvider(), DatabaseProvider(), GrpcioProvider())

    logfire.configure(service_name="track-service")

    logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
    logfire.instrument_sqlalchemy(engine=(await container.get(AsyncEngine)).sync_engine)
    logfire.instrument_asyncpg()

    server = grpc.aio.server(
        interceptors=[
            DishkaAioInterceptor(container)
        ]
    )
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    _health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
