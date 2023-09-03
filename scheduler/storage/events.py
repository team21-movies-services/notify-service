import logging
from time import sleep

import psycopg
from psycopg.rows import class_row

from core.config import Settings
from schemas import Event

logger = logging.getLogger(__name__)
RETRY_INTERVAL = 10


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

    def check_events(self):
        query = "SELECT * FROM events"
        try:
            self._ensure_connection()
            with self.connection.cursor(row_factory=class_row(Event)) as curr:  # type: ignore
                result = curr.execute(query)
                while True:
                    event = result.fetchone()
                    if not event:
                        logger.info("Подходящих событий нет, след проверка через {}c.".format(self.check_interval))
                        break
                    yield event
        except psycopg.OperationalError as e:
            logger.error("Ошибка подключения к бд: {}".format(e))
            sleep(RETRY_INTERVAL)
        finally:
            curr.close()

    def close_connection(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            logger.info("Соединение с базой данных закрыто.")
