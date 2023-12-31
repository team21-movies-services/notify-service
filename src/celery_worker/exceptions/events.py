from .base import BaseCeleryException


class EventCouldNotBeHandled(BaseCeleryException):
    """Event could not be handled"""


class CantGetUserIdException(BaseCeleryException):
    """Can't get user_id"""


class CannotParseEventData(BaseCeleryException):
    """Event data cannot be parsed"""
