from sqlalchemy.orm import Session

from app.models import Author
from app.repositories.base import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    def __init__(self, session: Session):
        super().__init__(Author, session)