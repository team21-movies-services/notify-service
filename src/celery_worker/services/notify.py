import logging
from dataclasses import dataclass
from typing import NoReturn

from celery_worker.exceptions.events import EventCouldNotBeHadnled
from celery_worker.repositories import TemplatesRepository
from celery_worker.utils.handlers_factory import HandlerFactoryProtocol
from shared.enums.notifications import NotificationTypesEnum
from shared.schemas.events import EventFilmsNewSchema, EventSchema, EventUsersNewSchema

logger = logging.getLogger(__name__)


@dataclass
class NotifyService:
    _template_repository: TemplatesRepository
    _handlers_factory: HandlerFactoryProtocol

    def process_event(self, event: EventSchema) -> None:
        match event.event_data:
            case EventUsersNewSchema():  # type: ignore[misc]
                users_list = [event.event_data.user_id]
                logger.info(users_list)
            case EventFilmsNewSchema():  # type: ignore[misc]
                # users_list = self._content_service.get_users_list(event.event_name)
                logger.info(event.event_name)
            case _ as unreachable:
                _asset_never(unreachable)

        notify_handler = self._handlers_factory.get(NotificationTypesEnum.email)
        logger.info(notify_handler)

        # rendered_template = notify_handler.render(content, template_body, template_wrapper)
        # notify_handler.send(users_list, rendered_template)


def _asset_never(event_name: str) -> NoReturn:
    raise EventCouldNotBeHadnled(event_name)
