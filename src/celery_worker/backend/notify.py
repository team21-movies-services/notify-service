import logging
from dataclasses import dataclass

from celery_worker.exceptions.handlers import HandlerHasntExistedYet
from celery_worker.repositories import TemplatesRepository
from celery_worker.schemas.content import ContentListSchema
from celery_worker.schemas.users import UserInfoList
from celery_worker.utils import (
    ContentServiceProtocol,
    HandlerFactoryProtocol,
    UserServiceProtocol,
)
from shared.enums.notifications import NotificationTypesEnum
from shared.exceptions.base import ObjectDoesNotExist
from shared.schemas.events import EventSchema

logger = logging.getLogger(__name__)


@dataclass
class NotifyBackend:
    _template_repository: TemplatesRepository
    _handlers_factory: HandlerFactoryProtocol
    _user_service: UserServiceProtocol
    _content_service: ContentServiceProtocol

    def process_event(self, event: EventSchema) -> None:
        users = self._user_service.get_users(event)
        content = self._content_service.get_content(event)
        self._send_notifications(event, users, content)

    def _send_notifications(self, event: EventSchema, users: UserInfoList, content: ContentListSchema) -> None:
        for notification_type in NotificationTypesEnum:
            try:
                handler = self._handlers_factory.get(notification_type)
                template = self._template_repository.get_by_event_and_notify(event.event_name, notification_type)
            except (HandlerHasntExistedYet, ObjectDoesNotExist) as err:
                logger.exception("Something went wrong", exc_info=err)
                continue

            filtered_users = list(filter(lambda user: notification_type in user.notifications, users))

            logger.info(handler)
            logger.info(template.name)
            logger.info(filtered_users)
            logger.info(content)

            # rendered_template = notify_handler.render(content, template)
            # notify_handler.send(filtered_users, rendered_template)
