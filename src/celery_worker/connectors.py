import logging
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Generator

import sentry_sdk
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from celery_worker.config import PostgresConfig, SentryConfig

logger = logging.getLogger(__name__)


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

    @contextmanager
    def get_db_session(self) -> Generator[Session, None, None]:
        with self.get_session() as session:
            yield session

    def close(self) -> None:
        self._engine.dispose()
        logger.info("DB connection has closed")


class SentryConnector:
    def __init__(self) -> None:
        config = SentryConfig()
        self._dsn = config.dsn

    def start_sentry(self):
        sentry_sdk.init(dsn=self._dsn,
                        traces_sample_rate=1.0,
                        profiles_sample_rate=1.0)

    def shutdown_sentry(self):
        client = sentry_sdk.Hub.current.client
        if client:
            client.close(timeout=2.0)


PGConnect: ContextVar[SyncPGConnect] = ContextVar('PGConnect')
