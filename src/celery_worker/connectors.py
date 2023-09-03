from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from celery_worker.config import PostgresConfig


class AsyncPGConnect:
    def __init__(self):
        config = PostgresConfig()
        self.async_engine = create_async_engine(
            config.database_url,
            echo=config.echo_log,
            max_overflow=20,
            pool_size=10,
        )
        self.async_session_maker = async_sessionmaker(
            self.async_engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autocommit=False,
            autoflush=False,
        )

    def get_session(self) -> AsyncSession:
        return self.async_session_maker()


class SyncPGConnect:
    def __init__(self):
        config = PostgresConfig()
        self._engine = create_engine(
            config.database_url,
            echo=config.echo_log,
            max_overflow=20,
            pool_size=10,
        )
        self._Session = sessionmaker(
            self._engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    def get_session(self) -> Session:
        return self._Session()

    def get_db_session(self) -> Generator[Session, None, None]:
        with self._Session() as session:
            yield session
