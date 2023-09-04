import logging.config
from time import sleep

from celery import Celery
from event_sender import send_event
from storage.events import PostgresEventStorage

from core.config import settings
from core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
CHECK_INTERVAL = settings.project.check_interval

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
)


def main():
    pg_storage = PostgresEventStorage(settings)
    try:
        while True:
            events = pg_storage.check_events()
            for event in events:
                send_event(app, event.model_dump())
            sleep(CHECK_INTERVAL)
    finally:
        pg_storage.close_connection()


if __name__ == '__main__':
    main()
