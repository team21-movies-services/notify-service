import logging
from dataclasses import dataclass
from typing import NoReturn

from celery_worker.exceptions.events import EventCouldNotBeHadnled
from celery_worker.repositories import TemplatesRepository
from celery_worker.utils.handlers_factory import HandlerFactoryProtocol
from shared.enums.events import EventNameEnum
from shared.enums.notifications import NotificationTypesEnum
from shared.schemas.events import EventSchema

logger = logging.getLogger(__name__)


@dataclass
class NotifyService:
    _template_repository: TemplatesRepository
    _handlers_factory: HandlerFactoryProtocol

    def process_event(self, event: EventSchema) -> None:
        match event.event_name:
            case EventNameEnum.users_created:
                logger.info(EventNameEnum.users_created)
            case EventNameEnum.films_new:
                logger.info(EventNameEnum.films_new)
            case _ as unreachable:
                _asset_never(unreachable)

        notify_handler = self._handlers_factory.get(NotificationTypesEnum.email)
        logger.info(notify_handler)

        # notify_handler.render()
        # notify_handler.send()


def _asset_never(event_name: str) -> NoReturn:
    raise EventCouldNotBeHadnled(event_name)
