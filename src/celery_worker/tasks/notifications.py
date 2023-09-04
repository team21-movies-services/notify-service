import logging

from pydantic_core import ValidationError
from requests import ConnectionError
from sqlalchemy.exc import OperationalError

from celery_worker.backend import NotifyBackend
from celery_worker.connectors import SyncPGConnect
from celery_worker.exceptions.base import BaseCeleryException
from celery_worker.main import app
from celery_worker.repositories import get_templates_repository
from celery_worker.utils import HandlersFactory, get_content_service, get_user_service
from shared.schemas.events import EventSchema
from shared.types.events import EventDict

logger = logging.getLogger(__name__)


@app.task(name="send_notification")
def send_notification(event: EventDict):
    logger.info("Get event: {event}".format(event=event))

    try:
        event_model = EventSchema.model_validate(event)
    except ValidationError as err:
        logger.exception("Event validation error", exc_info=err)
        # TODO: Вернуть event в очередь при возникновении ошибки
        return

    pg_connect = SyncPGConnect()

    try:
        handler_factory = HandlersFactory()
        user_service = get_user_service(event_model)
        template_repository = get_templates_repository(pg_connect)
        content_service = get_content_service(event_model)

        service = NotifyBackend(template_repository, handler_factory, user_service, content_service)
        service.process_event(event_model)
    except (ConnectionError, BaseCeleryException, OperationalError) as err:
        logger.exception("Getting some error.", exc_info=err)
        # TODO: Вернуть event в очередь при возникновении ошибки
    finally:
        pg_connect.close()
