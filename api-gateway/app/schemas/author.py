from uuid import UUID

from pydantic import BaseModel


class Author(BaseModel):
    id: UUID
    name: str
    genres: str