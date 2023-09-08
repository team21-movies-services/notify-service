from typing import NoReturn, Protocol

from celery_worker.exceptions.handlers import HandlerHasntExistedYet
from celery_worker.handlers import EmailHandlers, HandlerABC
from shared.enums.notifications import NotificationTypesEnum


class HandlerFactoryProtocol(Protocol):
    @staticmethod
    def get(event_type: NotificationTypesEnum) -> HandlerABC:
        ...


class HandlersFactory(HandlerFactoryProtocol):
    @staticmethod
    def get(event_type: NotificationTypesEnum) -> HandlerABC:
        match event_type:
            case NotificationTypesEnum.email:
                return EmailHandlers()
            # case NotificationTypesEnum.sms:
            #     return "sms handler"
            # case NotificationTypesEnum.push:
            #     return "push handler"
            case _ as unreachable:
                _asset_never(unreachable)


def _asset_never(event_type: str) -> NoReturn:
    raise HandlerHasntExistedYet(event_type)
