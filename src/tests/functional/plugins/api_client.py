import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture():
    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client
