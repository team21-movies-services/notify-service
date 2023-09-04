import logging.config
from time import sleep

from celery import Celery

from core.config import settings
from core.logger import LOGGING
from event_sender import send_notification
from storage.events import PostgresEventStorage

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
CHECK_INTERVAL = settings.project.check_interval

app = Celery(
    settings.celery.app_name,
    broker=settings.celery.broker,
    backend=settings.celery.backend,
)


def main():
    pg_storage = PostgresEventStorage(settings)
    try:
        while True:
            events = pg_storage.check_events()
            for event in events:
                send_notification(app, event.content)
                pg_storage.mark_event_as_completed(event)
            sleep(CHECK_INTERVAL)
    finally:
        pg_storage.close_connection()


if __name__ == '__main__':
    main()
