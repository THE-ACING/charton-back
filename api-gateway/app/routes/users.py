from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from app.auth import get_user
from app.schemas.playlist import Playlists
from app.schemas.user import User, UpdateUser, BindReferrerResponse, Users
from services.auth import auth_pb2
from services.playlist import playlist_pb2_grpc, playlist_pb2
from services.user import user_pb2_grpc, user_pb2

router = APIRouter(prefix="/users", tags=["user"], route_class=DishkaRoute)


@router.get("/{user_id}", response_model=User)
async def get_user_info(user_id: UUID, user_service: FromDishka[user_pb2_grpc.UserStub]) -> user_pb2.UserResponse:
    return await user_service.GetUser(user_pb2.UserRequest(id=str(user_id)))


@router.get("/{user_id}/playlists", response_model=Playlists)
async def get_playlists(
        user_id: UUID,
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
        limit: int = 10,
        offset: int = 0
) -> playlist_pb2.PlaylistsResponse:
    return await playlist_service.GetUserPlaylists(playlist_pb2.UserPlaylistsRequest(
        user_id=str(user_id),
        limit=limit,
        offset=offset
    ))


@router.get("/{user_id}/referrals", response_model=Users)
async def get_referrals(
        user_id: UUID,
        user_service: FromDishka[user_pb2_grpc.UserStub]
) -> user_pb2.UsersResponse:
    return await user_service.GetReferrals(user_pb2.ReferralsRequest(referrer_id=str(user_id)))


@router.post("/me", response_model=BindReferrerResponse)
async def set_referrer(user: Annotated[auth_pb2.UserResponse, Depends(get_user)], request: UpdateUser, user_service: FromDishka[user_pb2_grpc.UserStub]) -> user_pb2.BindReferrerResponse:
    return await user_service.BindReferrer(user_pb2.BindReferrerRequest(user_id=str(user.id), referrer_id=str(request.referrer_id)))
