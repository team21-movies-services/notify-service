from core.exceptions.base import AppException


class MongoException(AppException):
    """Base Mongo Exception"""


class BadCollectionResponseException(MongoException):
    """Bad response from mongo collection"""
