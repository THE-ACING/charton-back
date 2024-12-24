from typing import List
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    photo_url: str


class Users(BaseModel):
    users: List[User]


class UpdateUser(BaseModel):
    referrer_id: UUID


class BindReferrerResponse(BaseModel):
    success: bool
