import pytest_asyncio
from fastapi.testclient import TestClient

from app.dependencies.clients.get_ampq_connection import get_ws_ampq_connection
from app.main import app


@pytest_asyncio.fixture(name="ws_client", scope='session')
async def client_fixture(ampq_connect):
    def get_ampq_connect_override():
        return ampq_connect

    app.dependency_overrides[get_ws_ampq_connection] = get_ampq_connect_override

    client = TestClient(app)
    yield client
