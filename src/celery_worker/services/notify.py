import logging

from celery_worker.repositories import TemplatesRepository
from celery_worker.utils.handlers_factory import get_notification_handler
from shared.enums.notifications import NotificationTypesEnum
from shared.schemas.events import EventSchema

logger = logging.getLogger(__name__)


class NotifyService:
    def __init__(self, template_repository: TemplatesRepository) -> None:
        self._template_repository = template_repository

    def process_event(self, event: EventSchema) -> None:
        logger.info(event)
        notify_handler = get_notification_handler(NotificationTypesEnum.email)
        logger.info(notify_handler)
