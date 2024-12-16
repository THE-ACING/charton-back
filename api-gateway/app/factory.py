from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.routes.tracks import router as tracks_router
from app.routes.auth import router as auth_router


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


def create_app():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

    app.include_router(tracks_router)
    app.include_router(auth_router)

    return app
