from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.schemas.playlist import Playlists
from services.playlist import playlist_pb2_grpc, playlist_pb2

router = APIRouter(prefix="/user", tags=["user"], route_class=DishkaRoute)


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
