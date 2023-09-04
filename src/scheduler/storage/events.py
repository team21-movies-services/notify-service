import logging
from datetime import datetime

import psycopg
from psycopg.errors import OperationalError
from psycopg.rows import class_row
from utils import gen_backoff

from core.config import Settings
from schemas import Event

logger = logging.getLogger(__name__)
RETRY_INTERVAL = 10
BACKOFF_EXCEPTIONS = (OperationalError,)


class PostgresEventStorage:
    def __init__(self, settings: Settings):
        self.connection: psycopg.Connection | None = None  # type: ignore
        self.check_interval = settings.project.check_interval
        self.settings = settings

    def _connect(self):
        return psycopg.connect(str(self.settings.postgres.dsn))

    def _ensure_connection(self):
        if self.connection is None or self.connection.closed:
            logger.info("Подключение(повторное) к базе данных...")
            self.connection = self._connect()

    @gen_backoff(BACKOFF_EXCEPTIONS)
    def check_events(self):
        current_time = datetime.utcnow()
        query = "SELECT * FROM schedule WHERE completed = %s and start_time < %s"
        self._ensure_connection()
        with self.connection.cursor(row_factory=class_row(Event)) as curr:  # type: ignore
            result = curr.execute(query, (False, current_time))
            while True:
                event = result.fetchone()
                if not event:
                    logger.info("Подходящих событий нет, след проверка через {}c.".format(self.check_interval))
                    break
                yield event

    def close_connection(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Соединение с базой данных закрыто.")
