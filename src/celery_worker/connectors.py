import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from celery_worker.config import PostgresConfig

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

    def get_db_session(self) -> Generator[Session, None, None]:
        with self._Session() as session:
            yield session

    def close(self) -> None:
        self._engine.dispose()
        logger.info("DB connection has closed")
