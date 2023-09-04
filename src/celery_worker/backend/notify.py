import logging
from dataclasses import dataclass
from typing import NoReturn

from requests import Session as RequestSession

from celery_worker.config import NotificationsConfig
from celery_worker.exceptions.events import EventCouldNotBeHadnled
from celery_worker.exceptions.handlers import HandlerHasntExistedYet
from celery_worker.repositories import TemplatesRepository
from celery_worker.schemas.users import UserInfoSchema
from celery_worker.utils.handlers_factory import HandlerFactoryProtocol
from shared.enums.notifications import NotificationTypesEnum
from shared.exceptions.base import ObjectDoesNotExist
from shared.schemas.events import EventFilmsNewSchema, EventSchema, EventUsersNewSchema

logger = logging.getLogger(__name__)


@dataclass
class NotifyBackend:
    _template_repository: TemplatesRepository
    _handlers_factory: HandlerFactoryProtocol
    _client: RequestSession
    _config: NotificationsConfig

    def process_event(self, event: EventSchema) -> None:
        match event.event_data:
            case EventUsersNewSchema():  # type: ignore[misc]
                response = self._client.get(self._config.user_info_url.format(user_id=event.event_data.user_id))
            case EventFilmsNewSchema():  # type: ignore[misc]
                response = self._client.get(self._config.users_list_url.format(event_name=event.event_name))
            case _ as unreachable:
                _asset_never(unreachable)

        users_list = [UserInfoSchema(**user) for user in response.json()]
        # TODO: получение контента

        for notification_type in NotificationTypesEnum:
            try:
                handler = self._handlers_factory.get(notification_type)
                template = self._template_repository.get_by_event_and_notify(event.event_name, notification_type)
            except (HandlerHasntExistedYet, ObjectDoesNotExist) as err:
                logger.exception("Something went wrong", exc_info=err)
                continue

            users = list(filter(lambda user: notification_type in user.notifications, users_list))

            logger.info(handler)
            logger.info(template)
            logger.info(users)

            # rendered_template = notify_handler.render(content, template)
            # notify_handler.send(users, rendered_template)


def _asset_never(event_name: str) -> NoReturn:
    raise EventCouldNotBeHadnled(event_name)
