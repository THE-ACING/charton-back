import os
from dotenv import load_dotenv

import pytest
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi.testclient import TestClient
from uuid_extensions import uuid7

from app.factory import create_app
from app.settings import SettingsProvider
from app.utils import GrpcProvider


@pytest.fixture
def init_data():
    load_dotenv()
    return os.environ.get('INIT_DATA')


@pytest.fixture
def container():
    return make_async_container(SettingsProvider(), GrpcProvider())


@pytest.fixture
def app(container):
    app = create_app()
    setup_dishka(container=container, app=app)
    return app


@pytest.fixture
def client(app):
    return TestClient(app=app)


def test_get_playlists(client):
    response = client.get("/playlists?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "playlists" in data
    assert isinstance(data["playlists"], list)


def test_create_playlist(client, init_data):
    payload = {"title": "My Playlist", "thumbnail": "http://example.com/image.jpg"}
    response = client.post(
        "/playlists",
        json=payload,
        headers={"Authorization": f"Bearer { init_data }"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["thumbnail"] == payload["thumbnail"]


def test_get_playlist(client):
    playlist_id = str(uuid7())
    response = client.get(f"/playlists/{playlist_id}")
    if response.status_code == 200:  # Якщо плейлист існує
        data = response.json()
        assert data["id"] == playlist_id
        assert "title" in data
        assert "tracks" in data
    elif response.status_code == 404:  # Якщо плейлист не знайдено
        assert response.json()["detail"] == "Playlist not found"


def test_add_track_to_playlist(client):
    playlist_id = str(uuid7())
    track_payload = {"id": str(uuid7()), "title": "New Track"}
    response = client.post(f"/playlists/{playlist_id}/tracks", json=track_payload)
    if response.status_code == 200:
        data = response.json()
        assert any(track["id"] == track_payload["id"] for track in data["tracks"])
    elif response.status_code == 404:
        assert response.json()["detail"] == "Playlist not found"


def test_remove_track_from_playlist(client):
    playlist_id = str(uuid7())
    track_id = str(uuid7())
    response = client.delete(f"/playlists/{playlist_id}/tracks/{track_id}")
    if response.status_code == 200:
        data = response.json()
        assert all(track["id"] != track_id for track in data["tracks"])
    elif response.status_code == 404:
        assert response.json()["detail"] in ["Playlist not found", "Track not found"]


def test_get_user_playlists(client):
    user_id = str(uuid7())
    response = client.get(f"/user/{user_id}/playlists?limit=5&offset=0")
    if response.status_code == 200:
        data = response.json()
        assert "playlists" in data
        assert isinstance(data["playlists"], list)
    elif response.status_code == 404:
        assert response.json()["detail"] == "Not Found"


def test_get_tracks(client):
    response = client.get("/tracks?limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "tracks" in data
    assert isinstance(data["tracks"], list)


def test_search_tracks(client):
    query = "test"
    response = client.get(f"/tracks/search?query={query}&limit=5&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert "tracks" in data
    assert isinstance(data["tracks"], list)
