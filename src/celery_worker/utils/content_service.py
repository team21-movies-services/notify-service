from dataclasses import dataclass
from typing import Any, NoReturn, Protocol

from requests import Session as RequestSession

from celery_worker.config import APIsConfig
from celery_worker.exceptions.events import EventCouldNotBeHandled
from celery_worker.schemas.content import (
    ConfirmationUrlSchema,
    ContentListSchema,
    FilmsInfoSchema,
)
from celery_worker.utils.url_shortener import UrlShortenerService
from shared.schemas.events import EventFilmsNewSchema, EventSchema, EventUsersNewSchema


class ContentServiceProtocol(Protocol):
    def get_content(self, event: EventSchema) -> ContentListSchema:
        ...


@dataclass
class UserCreatedContentService(ContentServiceProtocol):
    _client: RequestSession
    _api: APIsConfig
    _url_shortener: UrlShortenerService

    def get_content(self, event: EventSchema) -> ContentListSchema:
        long_url = self._api.users.get_confirmation_uri.format(event.event_data.user_id)
        short_url = self._url_shortener.get_short_url(long_url)
        if short_url:
            return [ConfirmationUrlSchema(url=short_url)]
        return [ConfirmationUrlSchema(url=long_url)]


@dataclass
class NewFilmContentService(ContentServiceProtocol):
    _client: RequestSession
    _api: APIsConfig

    def get_content(self, event: EventSchema) -> ContentListSchema:
        response = self._client.get(self._api.films.new_uri.format(from_date=event.event_time))
        return [FilmsInfoSchema(**film) for film in response.json()]


def get_content_service(event: EventSchema) -> ContentServiceProtocol:
    client = RequestSession()
    api = APIsConfig()
    url_shortener = UrlShortenerService(client, api)

    match event.event_data:
        case EventUsersNewSchema():  # type: ignore[misc]
            # return UserCreatedContentService(client, api, )
            return UserCreatedContentService(client, api, url_shortener)
        case EventFilmsNewSchema():  # type: ignore[misc]
            return NewFilmContentService(client, api)
        case _ as unreachable:
            _asset_never(unreachable)


def _asset_never(event_name: Any) -> NoReturn:
    raise EventCouldNotBeHandled(event_name)
