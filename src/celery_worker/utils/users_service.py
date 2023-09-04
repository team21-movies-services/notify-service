from dataclasses import dataclass
from typing import Any, NoReturn, Protocol

from requests import Session as RequestSession

from celery_worker.config import APIsConfig
from celery_worker.exceptions.events import (
    CantGetUserIdException,
    EventCouldNotBeHandled,
)
from celery_worker.schemas.users import UserInfoList, UserInfoSchema
from shared.schemas.events import EventFilmsNewSchema, EventSchema, EventUsersNewSchema


class UserServiceProtocol(Protocol):
    def get_users(self, event: EventSchema) -> UserInfoList:
        ...


@dataclass
class CreatedUserService(UserServiceProtocol):
    _client: RequestSession
    _api: APIsConfig

    def get_users(self, event: EventSchema) -> UserInfoList:
        if isinstance(event.event_data, EventUsersNewSchema):
            response = self._client.get(self._api.users.info_uri.format(user_id=event.event_data.user_id))
            return [UserInfoSchema(**user) for user in response.json()]
        raise CantGetUserIdException


@dataclass
class NewFilmUserService(UserServiceProtocol):
    _client: RequestSession
    _api: APIsConfig

    def get_users(self, event: EventSchema) -> UserInfoList:
        response = self._client.get(self._api.users.list_uri.format(event_name=event.event_name))
        return [UserInfoSchema(**user) for user in response.json()]


def get_user_service(event: EventSchema) -> UserServiceProtocol:
    client = RequestSession()
    api = APIsConfig()

    match event.event_data:
        case EventUsersNewSchema():  # type: ignore[misc]
            return CreatedUserService(client, api)
        case EventFilmsNewSchema():  # type: ignore[misc]
            return NewFilmUserService(client, api)
        case _ as unreachable:
            _asset_never(unreachable)


def _asset_never(event_name: Any) -> NoReturn:
    raise EventCouldNotBeHandled(event_name)
