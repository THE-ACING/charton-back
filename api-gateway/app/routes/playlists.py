from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from app.auth import get_user
from app.schemas.playlist import Playlist, CreatePlaylist, PlaylistWithTracks, Track, Playlists
from app.schemas.user import User
from services.playlist import playlist_pb2, playlist_pb2_grpc

router = APIRouter(prefix="/playlists", tags=["playlists"], route_class=DishkaRoute)


@router.post("/", response_model=Playlist)
async def create_playlist(
        request: CreatePlaylist,
        user: Annotated[User, Depends(get_user)],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
) -> playlist_pb2.PlaylistResponse:
    return await playlist_service.CreatePlaylist(
        playlist_pb2.CreatePlaylistRequest(
            title=request.title,
            thumbnail=request.thumbnail
        ),
        metadata=(("user_id", str(user.id)),)
    )


@router.get("/{playlist_id}", response_model=PlaylistWithTracks)
async def get_playlist(
        playlist_id: UUID,
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
) -> playlist_pb2.PlaylistTracksResponse:
    return await playlist_service.GetPlaylist(playlist_pb2.PlaylistRequest(id=str(playlist_id)))


@router.put("/{playlist_id}", response_model=Playlist)
async def update_playlist(
        playlist_id: UUID,
        request: CreatePlaylist,
        user: Annotated[User, Depends(get_user)],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
):
    return await playlist_service.UpdatePlaylist(
        playlist_pb2.UpdatePlaylistRequest(
            id=str(playlist_id),
            title=request.title,
            thumbnail=request.thumbnail
        ),
        metadata=(("user_id", str(user.id)),),
    )


@router.delete("/{playlist_id}", response_model=Playlist)
async def remove_playlist(
        playlist_id: UUID,
        user: Annotated[User, Depends(get_user)],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
):
    return await playlist_service.RemovePlaylist(
        playlist_pb2.PlaylistRequest(id=str(playlist_id)),
        metadata=(("user_id", str(user.id)),),
    )


@router.post("/{playlist_id}/tracks", response_model=Playlist)
async def add_track_to_playlist(
        playlist_id: UUID,
        request: Track,
        user: Annotated[User, Depends(get_user)],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
):
    return await playlist_service.AddTrackToPlaylist(
        playlist_pb2.AddTrackToPlaylistRequest(
            playlist_id=str(playlist_id),
            track_id=str(request.id)
        ),
        metadata=(("user_id", str(user.id)),),
    )


@router.delete("/{playlist_id}/tracks/{track_id}", response_model=Playlist)
async def remove_track_from_playlist(
        playlist_id: UUID,
        track_id: UUID,
        user: Annotated[User, Depends(get_user)],
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
):
    return await playlist_service.RemoveTrackFromPlaylist(
        playlist_pb2.AddTrackToPlaylistRequest(
            playlist_id=str(playlist_id),
            track_id=str(track_id)
        ),
        metadata=(("user_id", str(user.id)),),
    )


@router.get("/", response_model=Playlists)
async def get_playlists(
        playlist_service: FromDishka[playlist_pb2_grpc.PlaylistStub],
        limit: int = 10,
        offset: int = 0,
):
    return await playlist_service.GetPlaylists(playlist_pb2.PlaylistsRequest(limit=limit, offset=offset))
