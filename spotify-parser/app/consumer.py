import io
import json
import logging
from contextlib import redirect_stdout
from time import sleep

import logfire
from b2sdk.v2 import B2Api, InMemoryAccountInfo
from kafka import KafkaConsumer
from spotdl import Spotdl, Song
from spotipy import Spotify, SpotifyClientCredentials
from yt_dlp import YoutubeDL

from app.database import session_maker, engine
from app.models import Track, Author
from app.repositories.author import AuthorRepository
from app.repositories.track import TrackRepository
from app.settings import settings
from app.stub import track_service
from services.track.track_pb2 import CreateAuthorRequest, CreateTrackRequest

instance = logfire.configure(service_name="spotify-parser")
logging.basicConfig(level=logging.INFO, handlers=[logfire.LogfireLoggingHandler()])
logfire.instrument_requests()
logfire.instrument_sqlalchemy(engine=engine)
logfire.instrument_psycopg()

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

for message in consumer:
    query = message.value.get('query')
    if not query:
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

            authors = []
            for artist in result['artists']:
                author = author_repository.find_one(Author.spotify_id == artist['id'])
                if not author:
                    sp_artist = sp.artist(f"spotify:artist:{artist['id']}")
                    logfire.info(f"Creating author: {artist['name']}", sp_artist=sp_artist)
                    new_author = track_service.CreateAuthor(CreateAuthorRequest(
                        name=artist['name'],
                        genres=",".join(sp_artist.get('genres', []))
                    ))
                    author = author_repository.create(Author(
                        id=new_author.id,
                        spotify_id=artist['id']
                    ))
                    session.commit()
                authors.append(author)

            song = Song.from_url(result['external_urls']['spotify'])
            urls = spotdl.get_download_urls([song])

            if not urls:
                logfire.info(f"Failed to get download urls for {song}")
                continue

            ctx = {
                "outtmpl": "-",
                "cookiefile": "/cookies.txt",
                'extract_audio': True,
                'format': 'bestaudio',
                'postprocessors': [
                    {
                        'key': 'FFmpegMetadata',
                        'add_metadata': True,
                    },
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '0',
                    },
                ],
                'extractor_args': {
                    'youtube': {
                        'player-client': ['web', 'default'],
                        'po_token': [f'web+{settings.PO_TOKEN.get_secret_value()}'],
                    },
                },
                'logtostderr': True
            }

            # with YoutubeDL() as ydl:
            #     info_dict = ydl.extract_info(urls[0], download=False)
            #     formats = info_dict.get('formats', [])
            #     logfire.info(f"Formats: {formats}", formats=formats)

            buffer = io.BytesIO()
            with redirect_stdout(buffer), YoutubeDL(ctx) as ydl:
                ydl.download(urls)

            file_version = tracks_bucket.upload_bytes(buffer.getvalue(), f"{result['id']}.mp3")
            track_repository.create(Track(author_id=author.id, spotify_id=result['id']))
            new_track = track_service.CreateTrack(CreateTrackRequest(
                title=result['name'],
                author_ids=[str(author.id) for author in authors],
                duration=result['duration_ms'] // 1000,
                source=tracks_bucket.get_download_url(file_version.file_name),
                thumbnail=result['album']['images'][0]['url']
            ))
            logfire.info(f"Created track: {new_track}", new_track=new_track)
            session.commit()
    sleep(5)