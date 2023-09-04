import logging
import time
from uuid import UUID

from celery import Celery

from celery_worker.connectors import SyncPGConnect
from celery_worker.repositories import TemplatesRepository

time.sleep(5)


logger = logging.getLogger(__name__)

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
    include=[
        "celery_worker.tasks.notifications",
    ],
)


@app.task(name="debug_task")
def add(x):
    return x


@app.task(name="get_template")
def get_template(template_id: UUID):
    pg_connect = SyncPGConnect()
    repository = TemplatesRepository(session=next(pg_connect.get_db_session()))
    logger.info(repository.get(template_id))
    pg_connect.close()
