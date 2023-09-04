import logging
import time
from uuid import UUID

from celery import Celery
from pydantic_core import ValidationError

from celery_worker.connectors import SyncPGConnect
from celery_worker.repositories import TemplatesRepository
from celery_worker.services import NotifyService
from shared.schemas.events import EventSchema
from shared.types.events import EventDict

time.sleep(5)


logger = logging.getLogger(__name__)

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
)


@app.task(name="debug_task")
def add(x, y):
    return x + y


@app.task(name="get_template")
def get_template(template_id: UUID):
    pg_connect = SyncPGConnect()
    repository = TemplatesRepository(session=next(pg_connect.get_db_session()))
    logger.info(repository.get(template_id))
    pg_connect.close()


@app.task(name="send_notification")
def send_notification(event: EventDict):
    logger.info("Get event: {event}".format(event=event))

    pg_connect = SyncPGConnect()
    repository = TemplatesRepository(session=next(pg_connect.get_db_session()))

    try:
        service = NotifyService(repository)
        service.process_event(EventSchema.model_validate(event))
    except ValidationError as err:
        logger.exception("Event validation error", exc_info=err)
    except Exception as err:
        logger.exception("get error", exc_info=err)
        # TODO: Вернуть event в очередь при возникновении ошибки
    finally:
        pg_connect.close()
