import logging.config
from time import sleep

import psycopg
from celery import Celery
from event_checker import check_for_events
from event_sender import send_event

from core.config import settings
from core.logger import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
CHECK_INTERVAL = settings.project.check_interval

host = settings
db_name = settings.postgres.db
user = settings.postgres.user
password = settings.postgres.password

pg_connect = psycopg.connect(str(settings.postgres.dsn))


def create_events_table(connection):
    cursor = connection.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()


app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
)


def main():
    while True:
        events = check_for_events(pg_connect)
        for event in events:
            send_event(app, event.model_dump())
        sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    create_events_table(pg_connect)
    main()
