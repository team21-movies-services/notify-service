from typing import NoReturn

from celery_worker.exceptions.events import HandlerHasntExistedYet
from shared.enums.notifications import NotificationTypesEnum


def get_notification_handler(event_type: NotificationTypesEnum) -> str:
    match event_type:
        case NotificationTypesEnum.email:
            return 'email handler'
        # case NotificationTypesEnum.sms:
        #     return "sms handler"
        # case NotificationTypesEnum.push:
        #     return "push handler"
        case _ as unreachable:
            _asset_never(unreachable)


def _asset_never(event_type: str) -> NoReturn:
    raise HandlerHasntExistedYet(event_type)
