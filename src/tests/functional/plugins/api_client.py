import pytest_asyncio
from aio_pika import connect
from celery import Celery
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.dependencies.clients.get_ampq_connection import get_ws_ampq_connection
from app.dependencies.clients.get_celery_app import get_celery_app
from app.dependencies.clients.get_db_session import get_db_session
from app.main import app


@pytest_asyncio.fixture(name="db_session", scope="session")
async def db_session():
    engine = create_async_engine(settings.postgres.database_url)

    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async with session_maker() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture(name="celery", scope="session")
async def celery_session():
    session = Celery(
        settings.celery.app_name,
        broker=settings.celery.broker,
        backend=settings.celery.backend,
    )
    yield session
    session.close()


@pytest_asyncio.fixture(name="ampq_connect", scope="session")
async def ampq_connect():
    connection = await connect(settings.ampq.broker)
    yield connection
    await connection.close()


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture(db_session, celery, ampq_connect):
    def get_session_override():
        return db_session

    def get_celery_override():
        return celery

    def get_ampq_connect_override():
        return ampq_connect

    app.dependency_overrides[get_db_session] = get_session_override
    app.dependency_overrides[get_celery_app] = get_celery_override
    app.dependency_overrides[get_ws_ampq_connection] = get_ampq_connect_override

    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client
