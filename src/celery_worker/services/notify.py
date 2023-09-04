import logging
from dataclasses import dataclass

from celery_worker.repositories import TemplatesRepository
from celery_worker.utils.handlers_factory import HandlerFactoryProtocol
from shared.enums.notifications import NotificationTypesEnum
from shared.schemas.events import EventSchema

logger = logging.getLogger(__name__)


@dataclass
class NotifyService:
    _template_repository: TemplatesRepository
    _handlers_factory: HandlerFactoryProtocol

    def process_event(self, event: EventSchema) -> None:
        logger.info(event)
        notify_handler = self._handlers_factory.get(NotificationTypesEnum.email)
        logger.info(notify_handler)

        # notify_handler.render()
        # notify_handler.send()
