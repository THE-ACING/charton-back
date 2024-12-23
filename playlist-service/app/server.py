import asyncio
import logging
from uuid import UUID

import grpc
import logfire
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, DishkaAioInterceptor, GrpcioProvider
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from grpc_interceptor.exceptions import NotFound, PermissionDenied
from sqlalchemy.orm import selectinload

from app.database import DatabaseProvider
from app.settings import SettingsProvider
from app.utils import GrpcProvider
from services.playlist import playlist_pb2, playlist_pb2_grpc
from app.models import Playlist, PlaylistTrack
from app.repositories.playlist import PlaylistRepository
from app.repositories.playlist_track import PlaylistTrackRepository
from services.track import track_pb2_grpc, track_pb2


class PlaylistServicer(playlist_pb2_grpc.PlaylistServicer):

    @inject
    async def CreatePlaylist(
            self,
            request: playlist_pb2.CreatePlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        user_id = dict(context.invocation_metadata()).get("user_id")

        playlist = await playlist_repository.create(Playlist(
            title=request.title,
            is_liked=request.is_liked,
            user_id=UUID(user_id),
            thumbnail=request.thumbnail
        ))
        await session.commit()
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def GetPlaylist(
            self,
            request: playlist_pb2.PlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository]
    ) -> playlist_pb2.PlaylistTracksResponse:
        playlist = await playlist_repository.get(UUID(request.id), options=[selectinload(Playlist.tracks)])
        if not playlist:
            raise NotFound("Playlist not found")
        return playlist_pb2.PlaylistTracksResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail,
            tracks=[str(track.track_id) for track in playlist.tracks]
        )

    @inject
    async def UpdatePlaylist(
            self,
            request: playlist_pb2.UpdatePlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repository.get(UUID(request.id))
        if not playlist:
            raise NotFound("Playlist not found")
        user_id = dict(context.invocation_metadata()).get("user_id")
        if playlist.user_id != UUID(user_id):
            raise PermissionDenied("You don't have permission to update this playlist")

        if request.title:
            playlist.title = request.title
        if request.thumbnail:
            playlist.thumbnail = request.thumbnail

        await session.commit()
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def RemovePlaylist(
            self,
            request: playlist_pb2.PlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repository.get(UUID(request.id))
        if not playlist:
            raise NotFound("Playlist not found")
        if playlist.is_liked:
            raise PermissionDenied("You don't have permission to remove this playlist")
        user_id = dict(context.invocation_metadata()).get("user_id")
        if playlist.user_id != UUID(user_id):
            raise PermissionDenied("You don't have permission to remove this playlist")

        await playlist_repository.delete(Playlist.id == playlist.id)
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def AddTrackToPlaylist(
            self,
            request: playlist_pb2.AddTrackToPlaylistRequest,
            context: grpc.aio.ServicerContext,
            track_service: FromDishka[track_pb2_grpc.TrackStub],
            playlist_repository: FromDishka[PlaylistRepository],
            playlist_track_repository: FromDishka[PlaylistTrackRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repository.get(UUID(request.playlist_id), options=[selectinload(Playlist.tracks)])
        if not playlist:
            raise NotFound("Playlist not found")
        user_id = dict(context.invocation_metadata()).get("user_id")
        if playlist.user_id != UUID(user_id):
            raise PermissionDenied("You don't have permission to add tracks to this playlist")

        try:
            await track_service.GetTrack(track_pb2.TrackRequest(id=request.track_id))
        except NotFound:
            raise NotFound("Track not found")

        playlist.tracks.append(
            await playlist_track_repository.create(PlaylistTrack(
                playlist_id=UUID(request.playlist_id),
                track_id=UUID(request.track_id)
            ))
        )
        await session.commit()
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def RemoveTrackFromPlaylist(
            self,
            request: playlist_pb2.AddTrackToPlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository],
            playlist_track_repository: FromDishka[PlaylistTrackRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repository.get(UUID(request.playlist_id))
        if not playlist:
            raise NotFound("Playlist not found")
        user_id = dict(context.invocation_metadata()).get("user_id")
        if playlist.user_id != UUID(user_id):
            raise PermissionDenied("You don't have permission to remove tracks from this playlist")

        track = await playlist_track_repository.find_one(PlaylistTrack.track_id == UUID(request.track_id), PlaylistTrack.playlist_id == UUID(request.playlist_id))
        if not track:
            raise NotFound("Track not found")
        await playlist_track_repository.delete(PlaylistTrack.id == track.id, PlaylistTrack.playlist_id == UUID(request.playlist_id))

        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            is_liked=playlist.is_liked,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def GetPlaylists(
            self,
            request: playlist_pb2.PlaylistsRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository]
    ) -> playlist_pb2.PlaylistsResponse:
        playlists = await playlist_repository.find(limit=request.limit, offset=request.offset)
        return playlist_pb2.PlaylistsResponse(
            playlists=[
                playlist_pb2.PlaylistResponse(
                    id=str(playlist.id),
                    title=playlist.title,
                    is_liked=playlist.is_liked,
                    thumbnail=playlist.thumbnail
                ) for playlist in playlists
            ]
        )

    @inject
    async def GetUserPlaylists(
            self,
            request: playlist_pb2.UserPlaylistsRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository]
    ) -> playlist_pb2.PlaylistsResponse:
        playlists = await playlist_repository.find(Playlist.user_id == UUID(request.user_id), limit=request.limit, offset=request.offset)
        return playlist_pb2.PlaylistsResponse(
            playlists=[
                playlist_pb2.PlaylistResponse(
                    id=str(playlist.id),
                    title=playlist.title,
                    is_liked=playlist.is_liked,
                    thumbnail=playlist.thumbnail
                ) for playlist in playlists
            ]
        )


async def serve():
    service_provider = Provider(scope=Scope.REQUEST)
    service_provider.provide(PlaylistRepository)
    service_provider.provide(PlaylistTrackRepository)
    container = make_async_container(service_provider, SettingsProvider(), DatabaseProvider(), GrpcProvider(), GrpcioProvider())

    logfire.configure(service_name="playlist-service")

    logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
    logfire.instrument_sqlalchemy(engine=(await container.get(AsyncEngine)).sync_engine)
    logfire.instrument_asyncpg()

    server = grpc.aio.server(
        interceptors=[
            DishkaAioInterceptor(container)
        ]
    )
    playlist_pb2_grpc.add_PlaylistServicer_to_server(PlaylistServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
