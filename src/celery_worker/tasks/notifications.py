import logging

from pydantic_core import ValidationError

from celery_worker.connectors import SyncPGConnect
from celery_worker.main import app
from celery_worker.repositories import TemplatesRepository
from celery_worker.services import NotifyService
from celery_worker.utils.handlers_factory import HandlersFactory
from shared.schemas.events import EventSchema
from shared.types.events import EventDict

logger = logging.getLogger(__name__)


@app.task(name="send_notification")
def send_notification(event: EventDict):
    logger.info("Get event: {event}".format(event=event))

    pg_connect = SyncPGConnect()
    template_repository = TemplatesRepository(session=next(pg_connect.get_db_session()))
    handler_factory = HandlersFactory()

    try:
        service = NotifyService(template_repository, handler_factory)
        service.process_event(EventSchema.model_validate(event))
    except ValidationError as err:
        logger.exception("Event validation error", exc_info=err)
    except Exception as err:
        logger.exception("get error", exc_info=err)
        # TODO: Вернуть event в очередь при возникновении ошибки
    finally:
        pg_connect.close()
