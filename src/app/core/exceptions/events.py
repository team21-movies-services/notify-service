from core.exceptions.base import AppException


class EventsException(AppException):
    """Base events exception"""


class NotificationException(EventsException):
    """Unknown notification type"""
