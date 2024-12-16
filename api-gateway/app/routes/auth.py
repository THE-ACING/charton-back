from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.user import User
from services.auth import auth_pb2
from services.auth.auth_pb2_grpc import AuthStub

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)

init_data_security = HTTPBearer(bearerFormat="Bearer")

@router.get("/init-data", response_model=User)
async def get_init_data(credentials: Annotated[HTTPAuthorizationCredentials, Depends(init_data_security)], auth_service: FromDishka[AuthStub]) -> auth_pb2.UserResponse:
    return await auth_service.GetUserByInitData(auth_pb2.InitDataRequest(init_data=credentials.credentials))