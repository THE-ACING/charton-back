from fastapi import FastAPI

from app.routes.tracks import router as tracks_router


def create_app():
    app = FastAPI()

    app.include_router(tracks_router)

    return app
