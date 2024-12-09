import io
import json
import logging
from contextlib import redirect_stdout

import logfire
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from kafka import KafkaConsumer

from opentelemetry.instrumentation.kafka import KafkaInstrumentor
from spotipy import Spotify, SpotifyClientCredentials
from spotdl import Spotdl, Song
from yt_dlp import YoutubeDL

from app.database import session_maker, engine
from app.models import Track, Author
from app.repositories.author import AuthorRepository
from app.repositories.track import TrackRepository
from app.settings import settings
from app.stub import track_service
from services.track.track_pb2 import CreateAuthorRequest, CreateTrackRequest

instance = logfire.configure(service_name="youtube-parser")
logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
logfire.instrument_requests()
logfire.instrument_sqlalchemy(engine=engine)
logfire.instrument_psycopg()
KafkaInstrumentor().instrument(
    tracer_provider=instance.config.get_tracer_provider(),
    meter_provider=instance.config.get_meter_provider()
)


consumer = KafkaConsumer(
    settings.KAFKA_TOPIC,
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", settings.B2_KEY_ID, settings.B2_APPLICATION_KEY)

tracks_bucket = b2_api.get_bucket_by_name(settings.B2_TRACK_BUCKET_NAME)

auth_manager = SpotifyClientCredentials(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET.get_secret_value()
)
sp = Spotify(auth_manager=auth_manager)
spotdl = Spotdl(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET.get_secret_value(),
    no_cache=True
)

# Consume messages from the topic
for message in consumer:
    query = message.value.get('query')
    if query is None:
        continue

    search_results = sp.search(query, type='track', limit=3)
    logfire.info(f"Search results for query '{query}': {search_results}", search_results=search_results)
    with session_maker() as session:
        track_repository = TrackRepository(session)
        author_repository = AuthorRepository(session)
        for result in search_results['tracks']['items']:
            logfire.info(f"Processing track: {result['name']}")

            if track_repository.find_one(Track.spotify_id == result['id']):
                logfire.info(f"Track already exists: {result['name']}")
                continue

            author = author_repository.find_one(Author.spotify_id == result['artists'][0]['id'])
            if not author:
                new_author = track_service.CreateAuthor(CreateAuthorRequest(
                    name=result['artists'][0]['name'],
                    genres=''
                ))
                author = author_repository.create(Author(
                    id=new_author.id,
                    spotify_id=result['artists'][0]['id'])
                )
                session.commit()

            song = Song.from_url(result['external_urls']['spotify'])
            urls = spotdl.get_download_urls([song])

            if not urls:
                logfire.info(f"Failed to get download urls for {song}")
                continue

            ctx = {
                "outtmpl": "-",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0',
                }],
                'logtostderr': True
            }

            buffer = io.BytesIO()
            with redirect_stdout(buffer), YoutubeDL(ctx) as ydl:
                ydl.download(urls)

            file_version = tracks_bucket.upload_bytes(buffer.getvalue(), f"{result['name']}.mp3")
            print(tracks_bucket.get_download_url(file_version.file_name))
            track = {
                "title": result['name'],
                "author_id": author.id,
                "duration": result['duration_ms'] // 1000,
                "source": tracks_bucket.get_download_url(file_version.file_name),
                "thumbnail": result['album']['images'][0]['url']
            }
            track_repository.create(Track(author_id=author.id, spotify_id=result['id']))
            logfire.info(track=track)
            new_track = track_service.CreateTrack(CreateTrackRequest(**track))
            logfire.info(f"Created track: {new_track}", new_track=new_track)
            session.commit()