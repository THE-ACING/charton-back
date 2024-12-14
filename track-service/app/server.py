import asyncio
import logging
from uuid import UUID

import grpc
import logfire
from aiokafka import AIOKafkaProducer
from dishka import FromDishka, make_async_container, Provider, Scope
from dishka.integrations.grpcio import inject, GrpcioProvider, DishkaAioInterceptor
from elasticsearch import AsyncElasticsearch
from grpc_interceptor.exceptions import NotFound
from grpc_health.v1 import health
from grpc_health.v1._async import _health_pb2_grpc # noqa
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import selectinload

from app.database import DatabaseProvider
from app.es import ElasticSearchProvider
from app.models import Track, Author
from app.producer import KafkaProvider
from app.repositories.author import AuthorRepository
from app.repositories.track import TrackRepository
from app.repositories.track_elasticsearch import TrackElasticsearchRepository, TrackElasticsearchProvider
from app.settings import Settings, SettingsProvider
from services.track import track_pb2
from services.track import track_pb2_grpc


class TrackServicer(track_pb2_grpc.TrackServicer):
    @inject
    async def CreateAuthor(self, request: track_pb2.CreateAuthorRequest, context: grpc.aio.ServicerContext, author_repository: FromDishka[AuthorRepository], session: FromDishka[AsyncSession]) -> track_pb2.AuthorResponse:
        author = await author_repository.create(Author(
            name=request.name,
            genres=request.genres
        ))
        await session.commit()
        return track_pb2.AuthorResponse(
            id=str(author.id),
            name=author.name,
            genres=author.genres
        )

    @inject
    async def CreateTrack(self, request: track_pb2.CreateTrackRequest, context: grpc.aio.ServicerContext, track_repository: FromDishka[TrackRepository], author_repository: FromDishka[AuthorRepository], session: FromDishka[AsyncSession]) -> track_pb2.TrackResponse:
        authors = []
        for author_id in request.author_ids:
            author = await author_repository.get(UUID(author_id))
            if author is None:
                raise NotFound("Author not found")
            authors.append(author)

        track = await track_repository.create(Track(
            title=request.title,
            authors=authors,
            duration=request.duration,
            source=request.source,
            thumbnail=request.thumbnail,
        ))
        await session.commit()
        return track_pb2.TrackResponse(
            id=str(track.id),
            title=track.title,
            authors=[track_pb2.Author(
                id=str(author.id),
                name=author.name,
                genres=author.genres
            ) for author in track.authors],
            duration=track.duration,
            source=track.source,
            thumbnail=track.thumbnail
        )

    @inject
    async def GetTrack(self, request: track_pb2.TrackRequest, context: grpc.aio.ServicerContext, track_repository: FromDishka[TrackRepository]) -> track_pb2.TrackResponse:
        track = await track_repository.get(UUID(request.id), options=[selectinload(Track.authors)])
        if track is None:
            raise NotFound("Track not found")
        return track_pb2.TrackResponse(
            id=str(track.id),
            title=track.title,
            authors=[track_pb2.Author(
                id=str(author.id),
                name=author.name,
                genres=author.genres
            ) for author in track.authors],
            duration=track.duration,
            source=track.source,
            thumbnail=track.thumbnail
        )

    @inject
    async def GetTracks(self, request: track_pb2.TracksRequest, context: grpc.aio.ServicerContext, track_repository: FromDishka[TrackRepository]) -> track_pb2.TracksResponse:
        tracks = await track_repository.find(limit=request.limit, offset=request.offset, options=[selectinload(Track.authors)])
        return track_pb2.TracksResponse(
            tracks=[track_pb2.TrackResponse(
                id=str(track.id),
                title=track.title,
                authors=[track_pb2.Author(
                    id=str(author.id),
                    name=author.name,
                    genres=author.genres
                ) for author in track.authors],
                duration=track.duration,
                source=track.source,
                thumbnail=track.thumbnail
            ) for track in tracks]
        )

    @inject
    async def SearchTracks(
            self,
            request: track_pb2.SearchRequest,
            context: grpc.aio.ServicerContext,
            settings: FromDishka[Settings],
            track_elasticsearch_repository: FromDishka[TrackElasticsearchRepository],
            producer: FromDishka[AIOKafkaProducer],
            track_repository: FromDishka[TrackRepository]
    ) -> track_pb2.TracksResponse:
        await producer.send(
            settings.PARSER_KAFKA_TOPIC,
            value={
                "query": request.query
            }
        )
        resp = await track_elasticsearch_repository.search(request.query, request.offset, request.limit)
        track_ids_order = {UUID(hit["_id"]): index for index, hit in enumerate(resp["hits"]["hits"])}

        tracks = await track_repository.find(Track.id.in_(UUID(hit["_id"]) for hit in resp["hits"]["hits"]), options=[selectinload(Track.authors)])
        tracks = sorted(tracks, key=lambda track: track_ids_order[track.id])

        return track_pb2.TracksResponse(
            tracks=[track_pb2.TrackResponse(
                id=str(track.id),
                title=track.title,
                authors=[track_pb2.Author(
                    id=str(author.id),
                    name=author.name,
                    genres=author.genres
                ) for author in track.authors],
                duration=track.duration,
                source=track.source,
                thumbnail=track.thumbnail
            ) for track in tracks]
        )


async def check_index(es: AsyncElasticsearch, settings: Settings) -> None:
    if await es.indices.exists(index=settings.ELASTICSEARCH_INDEX):
        return
    await es.indices.create(
        index=settings.ELASTICSEARCH_INDEX,
        body={
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "author": {
                        "type": "nested",
                        "properties": {
                            "name": {
                                "type": "text",
                                "analyzer": "standard"
                            },
                            "genres": {
                                "type": "text",
                                "analyzer": "standard"
                            }
                        }
                    }
                }
            }
        },
        ignore=400
    )


async def serve() -> None:
    service_provider = Provider(scope=Scope.REQUEST)
    service_provider.provide(TrackRepository)
    service_provider.provide(AuthorRepository)
    container = make_async_container(service_provider, SettingsProvider(), KafkaProvider(), ElasticSearchProvider(), DatabaseProvider(), TrackElasticsearchProvider(), GrpcioProvider())

    logfire.configure(service_name="track-service")

    logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
    logfire.instrument_sqlalchemy(engine=(await container.get(AsyncEngine)).sync_engine)
    logfire.instrument_asyncpg()

    await check_index(await container.get(AsyncElasticsearch), await container.get(Settings))

    server = grpc.aio.server(
        interceptors=[
            DishkaAioInterceptor(container)
        ]
    )
    track_pb2_grpc.add_TrackServicer_to_server(TrackServicer(), server)
    _health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
