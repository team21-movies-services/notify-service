from enum import StrEnum, auto


class NotificationTypesEnum(StrEnum):
    email = auto()
    push = auto()
    sms = auto()
    websocket = auto()
