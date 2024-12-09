from sqlalchemy.orm import Session

from app.models import Track
from app.repositories.base import BaseRepository


class TrackRepository(BaseRepository[Track]):
    def __init__(self, session: Session):
        super().__init__(Track, session)