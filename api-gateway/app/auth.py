from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth import auth_pb2
from services.auth.auth_pb2_grpc import AuthStub

init_data_security = HTTPBearer(bearerFormat="Bearer")


@inject
async def get_user(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(init_data_security)],
        auth_service: FromDishka[AuthStub]
) -> auth_pb2.UserResponse:
    return await auth_service.GetUserByInitData(auth_pb2.InitDataRequest(init_data=credentials.credentials))