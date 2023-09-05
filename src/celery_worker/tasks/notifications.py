import logging

from celery import Task
from pydantic_core import ValidationError
from requests import ConnectionError
from sqlalchemy.exc import OperationalError

from celery_worker.backend import NotifyBackend
from celery_worker.connectors import PGConnect
from celery_worker.exceptions.base import BaseCeleryException
from celery_worker.main import app
from celery_worker.repositories import get_templates_repository
from celery_worker.utils import HandlersFactory, get_content_service, get_user_service
from shared.schemas.events import EventSchema
from shared.types.events import EventDict

logger = logging.getLogger(__name__)


@app.task(name="send_notification", bind=True, default_retry_delay=60, max_retries=5)
def send_notification(self: Task, event: EventDict):
    logger.info("Get event: {event}".format(event=event))

    try:
        event_model = EventSchema.model_validate(event)
    except ValidationError as err:
        logger.exception("Event validation error", exc_info=err)
        return self.retry(exc=err)
    try:
        handler_factory = HandlersFactory()
        user_service = get_user_service(event_model)
        template_repository = get_templates_repository(PGConnect.get())
        content_service = get_content_service(event_model)

        service = NotifyBackend(template_repository, handler_factory, user_service, content_service)
        service.process_event(event_model)
    except (ConnectionError, BaseCeleryException, OperationalError) as err:
        logger.exception("Getting some error.", exc_info=err)
        return self.retry(exc=err)
