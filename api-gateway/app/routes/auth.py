from typing import Annotated

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter
from fastapi.params import Depends

from app.auth import get_user
from app.schemas.user import User
from services.auth import auth_pb2

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)



@router.get("/init-data", response_model=User)
async def get_init_data(user: Annotated[auth_pb2.UserResponse, Depends(get_user)]) -> auth_pb2.UserResponse:
    return user