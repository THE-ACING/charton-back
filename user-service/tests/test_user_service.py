from uuid import uuid4

import grpc
import pytest
from unittest.mock import AsyncMock

from grpc_interceptor.exceptions import NotFound
from dishka.integrations import grpcio

from app.models import User
from services.user import user_pb2
from app.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


def mock_fake_inject(func):
    return func


@pytest.fixture
def session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def user_repository():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_servicer(monkeypatch, session, user_repository):
    monkeypatch.setattr(grpcio, "inject", mock_fake_inject)

    from app.server import UserServicer

    servicer = UserServicer()
    return servicer


@pytest.fixture
def context():
    return AsyncMock(spec=grpc.aio.ServicerContext)


@pytest.mark.asyncio
async def test_create_user(user_servicer, user_repository, session, context):
    mock_user = User(id=uuid4())
    user_repository.create.return_value = mock_user

    response = await user_servicer.CreateUser(user_pb2.CreateUserRequest(), context, user_repository, session)

    session.commit.assert_called_once()
    assert response.id == str(mock_user.id)


@pytest.mark.asyncio
async def test_get_user(user_servicer, user_repository, context):

    mock_user = User(id=uuid4())
    user_repository.get.return_value = mock_user

    request = user_pb2.UserRequest(id=str(mock_user.id))
    context = AsyncMock()

    response = await user_servicer.GetUser(request, context, user_repository)

    user_repository.get.assert_called_once_with(mock_user.id)
    assert response.id == str(mock_user.id)


@pytest.mark.asyncio
async def test_get_user_not_found(user_servicer, user_repository, context):
    user_repository.get.return_value = None

    request = user_pb2.UserRequest(id=str(uuid4()))

    with pytest.raises(NotFound):
        await user_servicer.GetUser(request, context, user_repository)

    user_repository.get.assert_called_once()


@pytest.mark.asyncio
async def test_delete_user(user_servicer, user_repository, session, context):
    mock_user = User(id=uuid4())
    user_repository.get.return_value = mock_user

    request = user_pb2.UserRequest(id=str(mock_user.id))

    response = await user_servicer.DeleteUser(request, context, user_repository, session)

    user_repository.get.assert_called_once_with(mock_user.id)
    # user_repository.delete.assert_called_once_with(User.id == mock_user.id)
    session.commit.assert_called_once()

    assert response.id == str(mock_user.id)


@pytest.mark.asyncio
async def test_delete_user_not_found(user_servicer, user_repository, context, session):
    user_repository.get.return_value = None

    request = user_pb2.UserRequest(id=str(uuid4()))
    context = AsyncMock()

    with pytest.raises(NotFound):
        await user_servicer.DeleteUser(request, context, user_repository, session)

    user_repository.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_users(user_servicer, user_repository, context):
    mock_users = [User(id=uuid4()), User(id=uuid4())]
    user_repository.find.return_value = mock_users

    request = user_pb2.UsersRequest(limit=10, offset=0)
    context = AsyncMock()

    response = await user_servicer.GetUsers(request, context, user_repository)

    user_repository.find.assert_called_once_with(limit=10, offset=0)
    assert len(response.users) == len(mock_users)
    assert all(response.users[i].id == str(mock_users[i].id) for i in range(len(mock_users)))