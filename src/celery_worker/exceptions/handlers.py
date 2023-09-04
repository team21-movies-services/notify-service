from .base import BaseCeleryException


class HandlerHasntExistedYet(BaseCeleryException):
    """Handler hasn't existed yet"""
