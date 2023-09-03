import logging

from psycopg import Connection
from psycopg.rows import class_row

from core.config import settings
from schemas import Event

logger = logging.getLogger(__name__)


def check_for_events(connection: Connection):
    """
    Функция для проверки наступивших событий в базе данных.
    """
    logger.info("Проверка подходящих событий в базе данных")
    with connection and connection.cursor(row_factory=class_row(Event)) as curr:
        query = "SELECT * FROM events"
        result = curr.execute(query)
        while True:
            event = result.fetchone()
            if not event:
                logger.info(f"Подходящих событий нет, след проверка через {settings.project.check_interval}c")
                break
            yield event
