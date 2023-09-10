from uuid import uuid4

import pytest_asyncio

from app.dependencies.auth import get_ws_auth_data
from app.main import app
from app.schemas.auth import AuthData


@pytest_asyncio.fixture(name='auth_user', scope='session')
async def auth_user_fixture():
    yield AuthData(user_id=uuid4(), is_superuser=False)


@pytest_asyncio.fixture(name='auth_user_ws', scope='function')
async def auth_user_ws_fixture(auth_user):
    def get_auth_override():
        return auth_user, "SUCCESS"

    app.dependency_overrides[get_ws_auth_data] = get_auth_override
    yield get_auth_override()
    app.dependency_overrides[get_ws_auth_data] = get_ws_auth_data


@pytest_asyncio.fixture(name='forbidden_access_token', scope='function')
async def forbidden_token_fixture(get_forbidden_token: str):
    """Enable auth and return bad access token than disable auth"""

    yield get_forbidden_token


@pytest_asyncio.fixture(name='expire_access_token', scope='function')
async def expire_token_fixture(get_expire_token: str):
    """Enable auth and return expire access token than disable auth"""

    yield get_expire_token
