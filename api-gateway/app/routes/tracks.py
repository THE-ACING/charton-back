from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.schemas.tracks import Track, Tracks
from services.track import track_pb2, track_pb2_grpc

router = APIRouter(prefix="/tracks", tags=["tracks"], route_class=DishkaRoute)

@router.get("/")
async def get_tracks(track_service: FromDishka[track_pb2_grpc.TrackStub], limit: int = 10, offset: int = 0) -> Tracks:
    return await track_service.GetTracks(track_pb2.TracksRequest(limit=limit, offset=offset))


@router.get("/search")
async def search_tracks(track_service: FromDishka[track_pb2_grpc.TrackStub], query: str, limit: int = 10, offset: int = 0) -> Tracks:
    result = await track_service.SearchTracks(track_pb2.SearchRequest(
        query=query,
        limit=limit,
        offset=offset
    ))
    return result


@router.get("/{track_id}")
async def get_track(track_service: FromDishka[track_pb2_grpc.TrackStub], track_id: UUID) -> Track:
    return await track_service.GetTrack(track_pb2.TrackRequest(id=str(track_id)))
