import asyncio
import logging

import grpc
import logfire
from aiogram.utils.web_app import safe_parse_webapp_init_data
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, GrpcioProvider, DishkaAioInterceptor
from grpc_health.v1 import health
from grpc_health.v1._async import _health_pb2_grpc  # noqa
from grpc_interceptor.exceptions import Unauthenticated
from sqlalchemy.ext.asyncio import AsyncEngine

from app.database import DatabaseProvider
from app.models import TelegramUser
from app.repositories.telegram_user import TelegramUserRepository
from app.settings import SettingsProvider, Settings
from app.utils import GrpcProvider
from services.auth import auth_pb2, auth_pb2_grpc
from services.user import user_pb2, user_pb2_grpc


class AuthServicer(auth_pb2_grpc.AuthServicer):
    @inject
    async def GetUserByInitData(
            self,
            request: auth_pb2.InitDataRequest,
            context: grpc.aio.ServicerContext,
            settings: FromDishka[Settings],
            telegram_user_repository: FromDishka[TelegramUserRepository],
            user_service: FromDishka[user_pb2_grpc.UserStub]
    ) -> auth_pb2.UserResponse:
        try:
            data = safe_parse_webapp_init_data(token=settings.BOT_TOKEN.get_secret_value(), init_data=request.init_data)
        except ValueError:
            raise Unauthenticated("Invalid init data signature")

        telegram_user = await telegram_user_repository.find_one(TelegramUser.telegram_id == data.user.id)

        if telegram_user:
            user = await user_service.GetUser(user_pb2.UserRequest(id=str(telegram_user.id)))
        else:
            user = await user_service.CreateUser(user_pb2.CreateUserRequest())
            await telegram_user_repository.create(TelegramUser(id=user.id, telegram_id=data.user.id))

        return auth_pb2.UserResponse(id=str(user.id))


async def serve() -> None:
    service_provider = Provider(scope=Scope.REQUEST)
    service_provider.provide(TelegramUserRepository)
    container = make_async_container(service_provider, SettingsProvider(), DatabaseProvider(), GrpcProvider(), GrpcioProvider())

    logfire.configure(service_name="auth-service")

    logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
    logfire.instrument_sqlalchemy(engine=(await container.get(AsyncEngine)).sync_engine)
    logfire.instrument_asyncpg()

    server = grpc.aio.server(
        interceptors=[
            DishkaAioInterceptor(container)
        ]
    )
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    _health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
