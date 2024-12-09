import asyncio
import logging
from uuid import UUID

import grpc
import logfire
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, DishkaAioInterceptor, GrpcioProvider
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from grpc_interceptor.exceptions import NotFound

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
            playlist_repo: FromDishka[PlaylistRepository],
            session: FromDishka[AsyncSession]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repo.create(Playlist(
            title=request.title,
            thumbnail=request.thumbnail or ''
        ))
        await session.commit()
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            thumbnail=playlist.thumbnail
        )

    @inject
    async def GetPlaylist(
            self,
            request: playlist_pb2.PlaylistRequest,
            context: grpc.aio.ServicerContext,
            playlist_repository: FromDishka[PlaylistRepository]
    ) -> playlist_pb2.PlaylistResponse:
        playlist = await playlist_repository.get(UUID(request.id))
        if not playlist:
            raise NotFound("Playlist not found")
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
            thumbnail=playlist.thumbnail
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

        if request.title:
            playlist.title = request.title
        if request.thumbnail:
            playlist.thumbnail = request.thumbnail

        await session.commit()
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
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
        await playlist_repository.delete(playlist)
        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
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
        playlist = await playlist_repository.get(UUID(request.playlist_id))
        if not playlist:
            raise NotFound("Playlist not found")

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
        return await self.GetPlaylist(playlist_pb2.PlaylistRequest(id=request.playlist_id), context)

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
        track = await playlist_track_repository.get(UUID(request.track_id))
        if not track:
            raise NotFound("Track not found")
        playlist.tracks.remove(track)
        await session.commit()

        return playlist_pb2.PlaylistResponse(
            id=str(playlist.id),
            title=playlist.title,
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
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
